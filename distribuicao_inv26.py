"""
Algoritmo de Distribuição Inicial — Fábula INV26
Distribuição da coleção Inverno 2026 entre as 10 lojas físicas.

Decisões do time:
  - Prioridade quando estoque < demanda: leadtime decrescente (lojas mais distantes primeiro)
  - Completude de grade: >= 25% dos tamanhos ativos devem ter >= 1 unidade
    (rebaixado de 50% para não bloquear distribuições de 1 unidade em produtos com 4 tamanhos)
  - Mínimo de envio: 1 unidade (para demanda_arredondada >= 1)
  - Fonte de demanda: velocidade_prevista_inv26_v4.csv (calibrado ao INV25 real x crescimento)

Constraints obrigatórios:
  - SORTIMENTO = NAO -> zero unidades para aquela filial-produto-cor
  - Soma por produto-cor-tamanho <= TAM_N do arquivo de compra
  - Apenas inteiros >= 1 no output (linhas com 0 omitidas)
  - E-commerce excluido (nao esta no escopo — nao aparece nos arquivos de entrada)

Output: distribuicao_inv26.csv
  Colunas: FILIAL, PRODUTO, COR_PRODUTO, TAMANHO, QTD_DISTRIBUIR
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path("C:/Users/IIA/Documents/hackathon-azzas")

# ─── 1. Carregar inputs ───────────────────────────────────────────────────────
compra    = pd.read_excel(BASE / "docs/pilares/compras-dados/compra_INV26_lancamento_fabula.xlsx")
sort_raw  = pd.read_excel(BASE / "docs/pilares/compras-dados/sortimento_INV26_lancamento_fabula.xlsx")
leadtimes = pd.read_excel(BASE / "docs/pilares/compras-dados/leadtimes_INV26_lancamento_fabula.xlsx")
vel       = pd.read_csv(BASE / "velocidade_prevista_inv26_v4.csv")

print(f"Compra: {len(compra)} produto-cor, {compra['COMPRA'].sum()} pecas totais")
print(f"Sortimento: {len(sort_raw)} linhas, {(sort_raw['SORTIMENTO'] != 'SIM').sum()} NAO")
print(f"Velocidade v3: {len(vel)} linhas")

# ─── 2. Pre-processar tipos ───────────────────────────────────────────────────
# PRODUTO como float nos 3 arquivos — manter consistente para join
compra["PRODUTO"]   = compra["PRODUTO"].astype(float)
sort_raw["PRODUTO"] = sort_raw["PRODUTO"].astype(float)
vel["PRODUTO"]      = vel["PRODUTO"].astype(float)

TAM_COLS    = ["TAM_1","TAM_2","TAM_3","TAM_4","TAM_5","TAM_6"]
GRADE_THRESH = 0.25  # >= 25% dos tamanhos ativos precisam ter >= 1 unidade

# Fator de segurança: amplifica a demanda prevista antes da distribuição.
# Baseado no backtest INV25: MAPE=56% ao nível produto-loja; P70 do erro = 1,21.
# O KNN reduz parte da incerteza (agrupa similares), portanto 1,25 cobre a maioria
# dos cenários sem comprometer o CD regulador (+1,4% do estoque total).
SAFETY_FACTOR = 1.25

# Recomputa demanda_arredondada com o fator de segurança aplicado à demanda_prevista
vel["demanda_arredondada"] = (vel["demanda_prevista"] * SAFETY_FACTOR).apply(
    lambda x: max(1, round(x)) if x >= 0.3 else 0
)

# ─── 3. Construir lookup de sortimento ───────────────────────────────────────
# SIM = pode enviar; qualquer outro valor = nao pode
sort_sim = set(
    zip(
        sort_raw[sort_raw["SORTIMENTO"] == "SIM"]["FILIAL"],
        sort_raw[sort_raw["SORTIMENTO"] == "SIM"]["PRODUTO"],
        sort_raw[sort_raw["SORTIMENTO"] == "SIM"]["COR_PRODUTO"],
    )
)

def is_elegivel(filial, produto, cor):
    return (filial, produto, cor) in sort_sim

# ─── 4. Lookup de leadtime por filial ─────────────────────────────────────────
lt_map = dict(zip(leadtimes["FILIAL"], leadtimes["LEADTIME"]))

# ─── 5. Algoritmo de distribuição ────────────────────────────────────────────

def largest_remainder(quota, weights):
    """
    Distribui `quota` unidades inteiras de acordo com `weights` (dict tam -> frac).
    Usa o metodo do maior resto para minimizar erro de arredondamento.
    Retorna dict tam -> int.
    """
    tams = list(weights.keys())
    raw  = {t: quota * weights[t] for t in tams}
    int_alloc = {t: int(v) for t, v in raw.items()}
    needed    = quota - sum(int_alloc.values())
    remainders = sorted(tams, key=lambda t: raw[t] - int_alloc[t], reverse=True)
    for t in remainders[:needed]:
        int_alloc[t] += 1
    return int_alloc

output_rows = []
stats = {
    "produto_cor_processados": 0,
    "filial_produto_cor_enviados": 0,
    "filial_produto_cor_zerados_sortimento": 0,
    "filial_produto_cor_zerados_grade": 0,
    "filial_produto_cor_zerados_estoque": 0,
    "pecas_total_distribuidas": 0,
}

for _, row_c in compra.iterrows():
    produto = row_c["PRODUTO"]
    cor     = int(row_c["COR_PRODUTO"])
    stats["produto_cor_processados"] += 1

    # Estoque disponivel por tamanho
    stock = {t: int(row_c[t]) for t in TAM_COLS}
    active_tams  = [t for t in TAM_COLS if stock[t] > 0]
    n_active     = len(active_tams)
    total_stock  = sum(stock[t] for t in active_tams)

    if n_active == 0 or total_stock == 0:
        continue

    # Pesos de tamanho baseados no mix de compra
    size_weights = {t: stock[t] / total_stock for t in active_tams}

    # Demanda prevista para este produto-cor, apenas filiais elegiveis
    vel_pc = vel[
        (vel["PRODUTO"] == produto) &
        (vel["COR_PRODUTO"] == cor)
    ].copy()

    vel_pc["elegivel"] = vel_pc.apply(
        lambda r: is_elegivel(r["FILIAL"], r["PRODUTO"], r["COR_PRODUTO"]), axis=1
    )

    # Restrição de sortimento: filiais NAO -> demanda_arredondada = 0
    stats["filial_produto_cor_zerados_sortimento"] += (
        (~vel_pc["elegivel"] & (vel_pc["demanda_arredondada"] > 0)).sum()
    )

    vel_elig = vel_pc[vel_pc["elegivel"] & (vel_pc["demanda_arredondada"] > 0)].copy()

    if vel_elig.empty:
        continue

    total_demand = int(vel_elig["demanda_arredondada"].sum())

    # ── Alocação de quotas por filial ─────────────────────────────────────
    if total_demand <= total_stock:
        # Estoque suficiente: cada filial recebe sua demanda integral
        quotas = dict(zip(vel_elig["FILIAL"], vel_elig["demanda_arredondada"].astype(int)))
    else:
        # Estoque insuficiente: priorizar por leadtime decrescente (lojas mais distantes primeiro)
        vel_sorted = vel_elig.sort_values("LEADTIME", ascending=False).reset_index(drop=True)
        quotas = {}
        remaining = total_stock
        for _, vrow in vel_sorted.iterrows():
            if remaining <= 0:
                break
            q = min(int(vrow["demanda_arredondada"]), remaining)
            if q > 0:
                quotas[vrow["FILIAL"]] = q
                remaining -= q
        stats["filial_produto_cor_zerados_estoque"] += (
            len(vel_elig) - len(quotas)
        )

    # ── Distribuição por tamanho dentro de cada filial ────────────────────
    # Rastreamento de estoque usado por tamanho para garantir constraint
    size_used = {t: 0 for t in active_tams}

    for filial, quota in quotas.items():
        if quota <= 0:
            continue

        # Calcular disponibilidade restante por tamanho
        avail = {t: stock[t] - size_used[t] for t in active_tams}
        avail_active = {t: v for t, v in avail.items() if v > 0}
        total_avail  = sum(avail_active.values())

        if total_avail <= 0:
            stats["filial_produto_cor_zerados_estoque"] += 1
            continue

        # Capear quota ao disponivel restante
        quota_efetivo = min(quota, total_avail)

        # Pesos baseados na disponibilidade restante (respeita constraint por tamanho)
        weights_eff = {t: avail_active[t] / total_avail for t in avail_active}

        # Arredondamento pelo maior resto
        alloc = largest_remainder(quota_efetivo, weights_eff)

        # Verificacao de completude de grade
        # >= 25% dos tamanhos ativos devem ter >= 1 unidade (permite 1 unidade em grade de 4)
        n_filled = sum(1 for t in active_tams if alloc.get(t, 0) >= 1)
        if n_filled < n_active * GRADE_THRESH:
            stats["filial_produto_cor_zerados_grade"] += 1
            continue

        # Gravar alocação
        total_filial = 0
        for t in active_tams:
            qty = alloc.get(t, 0)
            if qty >= 1:
                tam_num = int(t.replace("TAM_", ""))
                output_rows.append({
                    "FILIAL":        filial,
                    "PRODUTO":       produto,
                    "COR_PRODUTO":   cor,
                    "TAMANHO":       tam_num,
                    "QTD_DISTRIBUIR": qty,
                })
                size_used[t] += qty
                total_filial  += qty

        if total_filial > 0:
            stats["filial_produto_cor_enviados"] += 1
            stats["pecas_total_distribuidas"]   += total_filial

# ─── 6. Montar DataFrame de output ───────────────────────────────────────────
dist = pd.DataFrame(output_rows)

if dist.empty:
    print("AVISO: nenhuma linha gerada!")
else:
    # Ordenar por filial, produto, cor, tamanho
    dist = dist.sort_values(["FILIAL","PRODUTO","COR_PRODUTO","TAMANHO"]).reset_index(drop=True)

    # ─── 7. Validações obrigatórias ──────────────────────────────────────────
    print("\n=== VALIDACOES ===")
    erros = 0

    # V1: sem violação de sortimento
    sort_nao = set(
        zip(
            sort_raw[sort_raw["SORTIMENTO"] != "SIM"]["FILIAL"],
            sort_raw[sort_raw["SORTIMENTO"] != "SIM"]["PRODUTO"],
            sort_raw[sort_raw["SORTIMENTO"] != "SIM"]["COR_PRODUTO"],
        )
    )
    violacoes_sort = dist[
        dist.apply(lambda r: (r["FILIAL"], r["PRODUTO"], r["COR_PRODUTO"]) in sort_nao, axis=1)
    ]
    if len(violacoes_sort) > 0:
        print(f"[ERRO] Violacoes de sortimento: {len(violacoes_sort)}")
        print(violacoes_sort)
        erros += 1
    else:
        print("[OK] Zero violacoes de sortimento")

    # V2: soma por produto-cor-tamanho <= TAM_N do compra
    dist["tam_col"] = "TAM_" + dist["TAMANHO"].astype(str)
    soma_pc_tam = dist.groupby(["PRODUTO","COR_PRODUTO","tam_col"])["QTD_DISTRIBUIR"].sum().reset_index()
    compra_melt = compra.melt(
        id_vars=["PRODUTO","COR_PRODUTO"],
        value_vars=TAM_COLS,
        var_name="tam_col",
        value_name="tam_disponivel"
    )
    check = soma_pc_tam.merge(compra_melt, on=["PRODUTO","COR_PRODUTO","tam_col"], how="left")
    violacoes_est = check[check["QTD_DISTRIBUIR"] > check["tam_disponivel"]]
    if len(violacoes_est) > 0:
        print(f"[ERRO] Violacoes de estoque: {len(violacoes_est)} produto-cor-tamanho")
        print(violacoes_est.head(10))
        erros += 1
    else:
        print("[OK] Nenhuma violacao de estoque (soma <= TAM_N para todos)")

    # V3: todos os valores >= 1
    minimo = dist["QTD_DISTRIBUIR"].min()
    if minimo < 1:
        print(f"[ERRO] QTD_DISTRIBUIR com valor < 1: min={minimo}")
        erros += 1
    else:
        print(f"[OK] QTD_DISTRIBUIR minimo = {minimo}")

    # V4: sem e-commerce (nao deveria aparecer — por precaucao)
    ecomm = ["FABULA ECOMMERCE CM","FABULA ECOMMERCE SP CM"]
    ecomm_rows = dist[dist["FILIAL"].isin(ecomm)]
    if len(ecomm_rows) > 0:
        print(f"[ERRO] E-commerce no output: {len(ecomm_rows)} linhas")
        erros += 1
    else:
        print("[OK] Nenhuma linha de e-commerce")

    if erros == 0:
        print("\nTodas as validacoes passaram.")
    else:
        print(f"\n{erros} validacao(oes) com ERRO — revisar antes de usar.")

    # ─── 8. Sumário ──────────────────────────────────────────────────────────
    print("\n=== SUMARIO DE DISTRIBUICAO ===")
    print(f"Produto-cor processados:          {stats['produto_cor_processados']}")
    print(f"Filial-produto-cor enviados:       {stats['filial_produto_cor_enviados']}")
    print(f"  Zerados por sortimento NAO:      {stats['filial_produto_cor_zerados_sortimento']}")
    print(f"  Zerados por completude de grade: {stats['filial_produto_cor_zerados_grade']}")
    print(f"  Zerados por falta de estoque:    {stats['filial_produto_cor_zerados_estoque']}")
    print(f"Pecas totais distribuidas:         {stats['pecas_total_distribuidas']}")
    print(f"Pecas retidas no CD (regulador):   {compra['COMPRA'].sum() - stats['pecas_total_distribuidas']}")
    pct = stats['pecas_total_distribuidas'] / compra['COMPRA'].sum() * 100
    print(f"Pct distribuido vs comprado:       {pct:.1f}%")
    print(f"\nLinhas no output:                  {len(dist)}")

    print("\n=== DISTRIBUICAO POR FILIAL ===")
    resumo_filial = dist.groupby("FILIAL").agg(
        pecas=("QTD_DISTRIBUIR","sum"),
        n_produto_cor=("PRODUTO","count"),
    )
    resumo_filial["n_produto_cor"] = dist.groupby("FILIAL").apply(
        lambda g: g[["PRODUTO","COR_PRODUTO"]].drop_duplicates().shape[0]
    )
    print(resumo_filial.sort_values("pecas", ascending=False).to_string())

    print("\n=== TOP 10 PRODUTO-COR POR DEMANDA TOTAL ===")
    top_pc = (
        dist.groupby(["PRODUTO","COR_PRODUTO"])["QTD_DISTRIBUIR"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    print(top_pc.to_string())

    # ─── 9. Salvar output ────────────────────────────────────────────────────
    out_cols = ["FILIAL","PRODUTO","COR_PRODUTO","TAMANHO","QTD_DISTRIBUIR"]
    dist[out_cols].to_csv(BASE / "distribuicao_inv26.csv", index=False)
    print(f"\nSalvo: {BASE / 'distribuicao_inv26.csv'}")
    print(f"Total de linhas: {len(dist)}")
