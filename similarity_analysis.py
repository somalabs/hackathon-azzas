"""
Análise de Similaridade INV26 — Fábula
Calcula similaridade entre produtos INV26 e histórico INV23/24/25
e estima velocidade de venda por loja.

Data-base: 31/03/2026
Canal: Varejo (lojas físicas)
Marca: Fábula
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path("C:/Users/IIA/Documents/hackathon-azzas")

# ─── 1. Carregar insumos ─────────────────────────────────────────────────────

compra    = pd.read_excel(BASE / "docs/pilares/compras-dados/compra_INV26_lancamento_fabula.xlsx")
sortimento = pd.read_excel(BASE / "docs/pilares/compras-dados/sortimento_INV26_lancamento_fabula.xlsx")
leadtimes  = pd.read_excel(BASE / "docs/pilares/compras-dados/leadtimes_INV26_lancamento_fabula.xlsx")
attrs_inv26 = pd.read_csv(BASE / "produtos_inv26_attrs.csv")
hist        = pd.read_csv(BASE / "historico_inv_vendas.csv")

print("=== INSUMOS CARREGADOS ===")
print(f"Compra:      {len(compra)} linhas (produto-cor)")
print(f"Sortimento:  {len(sortimento)} linhas")
print(f"Leadtimes:   {len(leadtimes)} filiais")
print(f"Attrs INV26: {len(attrs_inv26)} produtos únicos no catálogo")
print(f"Histórico:   {len(hist)} linhas (produto-cor × filial × coleção)")

# ─── 2. Normalizar nomes de filial ────────────────────────────────────────────

STORE_MAP = {
    "FABULA SHOP LEBLON CM":   ["FABULA SHOP LEBLON CM", "FABULA LEBLON CM", "FABULA SHOP LEBLON"],
    "FABULA BARRA SHOPPING":   ["FABULA BARRA SHOPPING", "FABULA BARRA SHOP", "FABULA BARRA SHOPPI"],
    "FABULA RIO SUL CM":       ["FABULA RIO SUL CM", "FABULA RIO SUL"],
    "FABULA RDB CM":           ["FABULA RDB CM", "FABULA RDB"],
    "FABULA HARMONIA SP CM":   ["FABULA HARMONIA SP CM", "FABULA HARMONIA SP", "FABULA HARMONIA"],
    "FABULA PLAZA SHOP CM":    ["FABULA PLAZA SHOP CM", "FABULA PLAZA SHOP", "FABULA PLAZA"],
    "FABULA SHOP VITORIA CM":  ["FABULA SHOP VITORIA CM", "FABULA VITORIA CM", "FABULA VITORIA"],
    "FABULA BARRA SALVADOR CM":["FABULA BARRA SALVADOR CM", "FABULA BARRA SALVADOR", "FABULA SALVADOR"],
    "FABULA ELDORADO CM":      ["FABULA ELDORADO CM", "FABULA ELDORADO"],
    "FABULA CENTRO CM":        ["FABULA CENTRO CM", "FABULA CENTRO"],
}

# Build reverse map: variante → nome canônico
rev_map = {}
for canonical, variants in STORE_MAP.items():
    for v in variants:
        rev_map[v] = canonical

# Normalizar histórico
hist["filial_canon"] = hist["nome_filial"].map(rev_map)

# Quantas lojas INV26 mapeadas no histórico?
mapeadas = hist["filial_canon"].notna().sum()
print(f"\nLinhas históricas com filial mapeada: {mapeadas} / {len(hist)} ({mapeadas/len(hist)*100:.1f}%)")
print("Filiais históricas únicas mapeadas:", hist["filial_canon"].dropna().unique().tolist())

# Filiar apenas às 10 lojas INV26
hist_10 = hist[hist["filial_canon"].notna()].copy()
print(f"\nHistórico filtrado para 10 lojas INV26: {len(hist_10)} linhas")

# ─── 3. Calcular velocidade histórica por produto-cor × filial ────────────────

# Janela ON-season por coleção (dias aproximados)
ON_DAYS = {"INV23": 122, "INV24": 122, "INV25": 122}

# Peso por coleção (INV25 mais recente = maior peso)
PESO_COLECAO = {"INV23": 1.0, "INV24": 2.0, "INV25": 3.0}

hist_10 = hist_10.copy()
hist_10["on_days"]   = hist_10["COLECAO"].map(ON_DAYS)
hist_10["peso"]      = hist_10["COLECAO"].map(PESO_COLECAO)
hist_10["pecas_pos"] = hist_10["pecas_vendidas"].clip(lower=0)
hist_10["velocidade_dia"] = hist_10["pecas_pos"] / hist_10["on_days"]

# Agregar por produto-cor × filial (média ponderada por peso de coleção)
def weighted_velocity(group):
    total_peso = group["peso"].sum()
    vel = (group["velocidade_dia"] * group["peso"]).sum() / total_peso if total_peso > 0 else 0
    return pd.Series({
        "velocidade_dia":  vel,
        "pecas_total_hist": group["pecas_pos"].sum(),
        "colecoes":         "|".join(group["COLECAO"].unique()),
        "GRUPO_PRODUTO":    group["GRUPO_PRODUTO"].mode()[0] if not group["GRUPO_PRODUTO"].isna().all() else None,
        "LINHA":            group["LINHA"].mode()[0] if not group["LINHA"].isna().all() else None,
    })

vel_hist = (
    hist_10
    .groupby(["PRODUTO", "COR_PRODUTO", "filial_canon"])
    .apply(weighted_velocity, include_groups=False)
    .reset_index()
)

vel_hist["PRODUTO"] = vel_hist["PRODUTO"].astype(str)
print(f"\nVelocidades históricas calculadas: {len(vel_hist)} linhas (produto-cor × filial)")
print(f"Velocidade mediana: {vel_hist['velocidade_dia'].median():.4f} pcs/dia")
print(f"Velocidade máx: {vel_hist['velocidade_dia'].max():.4f} pcs/dia")

# ─── 4. Montar atributos de similaridade ─────────────────────────────────────

# INV26: combinar compra (que tem COR) com attrs (que tem GRUPO/LINHA)
compra["PRODUTO"] = compra["PRODUTO"].astype(str)
attrs_inv26["PRODUTO"] = attrs_inv26["PRODUTO"].astype(str)

inv26 = compra[["PRODUTO", "COR_PRODUTO", "DESCRICAO", "COMPRA"]].merge(
    attrs_inv26[["PRODUTO", "GRUPO_PRODUTO", "SUBGRUPO_PRODUTO", "LINHA"]],
    on="PRODUTO",
    how="left"
)

# Histórico: atributos por produto (sem cor — para similaridade de categoria)
hist_attrs = (
    hist_10[["PRODUTO", "COR_PRODUTO", "GRUPO_PRODUTO", "LINHA"]]
    .drop_duplicates()
    .dropna(subset=["GRUPO_PRODUTO"])
)
hist_attrs["PRODUTO"] = hist_attrs["PRODUTO"].astype(str)

print(f"\nProdutos INV26 com atributos: {inv26['GRUPO_PRODUTO'].notna().sum()} / {len(inv26)}")
print(f"Produtos históricos únicos para similaridade: {hist_attrs['PRODUTO'].nunique()}")

# ─── 5. Calcular similaridade ─────────────────────────────────────────────────

def compute_similarity(row_inv26, row_hist):
    """
    Pesos:
      GRUPO_PRODUTO   (tipo de peça: vestido, blusa...)  -> 0.55
      SUBGRUPO_PRODUTO (detalhe: curto, legging...)      -> 0.25
      LINHA           (tecido/material)                  -> 0.20
    """
    sim = 0.0
    if pd.notna(row_inv26["GRUPO_PRODUTO"]) and pd.notna(row_hist["GRUPO_PRODUTO"]):
        if row_inv26["GRUPO_PRODUTO"] == row_hist["GRUPO_PRODUTO"]:
            sim += 0.55
    if pd.notna(row_inv26.get("SUBGRUPO_PRODUTO")) and pd.notna(row_hist.get("SUBGRUPO_PRODUTO", None)):
        if row_inv26.get("SUBGRUPO_PRODUTO") == row_hist.get("SUBGRUPO_PRODUTO"):
            sim += 0.25
    if pd.notna(row_inv26["LINHA"]) and pd.notna(row_hist["LINHA"]):
        if row_inv26["LINHA"] == row_hist["LINHA"]:
            sim += 0.20
    return sim

# Para cada produto INV26, calcular a velocidade prevista por filial
# usando os K vizinhos mais próximos do histórico

TARGET_STORES = leadtimes["FILIAL"].tolist()
K_NEIGHBORS = 10  # top-K históricos mais similares

# Velocidade média histórica por filial (fallback para produtos sem similar)
vel_media_filial = (
    vel_hist.groupby("filial_canon")["velocidade_dia"]
    .agg(lambda x: x[x > 0].median() if (x > 0).any() else 0)
    .to_dict()
)

results = []

for _, row26 in inv26.iterrows():
    produto = row26["PRODUTO"]
    cor     = row26["COR_PRODUTO"]

    # Atributos INV26 para este produto
    grupo26     = row26.get("GRUPO_PRODUTO")
    subgrupo26  = row26.get("SUBGRUPO_PRODUTO")
    linha26     = row26.get("LINHA")

    # Se sem atributos, usar fallback de filial
    if pd.isna(grupo26):
        for filial in TARGET_STORES:
            results.append({
                "PRODUTO": produto, "COR_PRODUTO": cor, "FILIAL": filial,
                "velocidade_prevista": vel_media_filial.get(filial, 0),
                "n_similares": 0, "sim_media": 0.0, "metodo": "fallback_sem_attrs"
            })
        continue

    # Calcular similaridade com cada produto histórico
    sim_scores = []
    for _, row_h in hist_attrs.iterrows():
        sim = 0.0
        if pd.notna(grupo26) and pd.notna(row_h["GRUPO_PRODUTO"]):
            if grupo26 == row_h["GRUPO_PRODUTO"]:
                sim += 0.55
        if pd.notna(subgrupo26) and "SUBGRUPO_PRODUTO" in row_h and pd.notna(row_h.get("SUBGRUPO_PRODUTO")):
            if subgrupo26 == row_h["SUBGRUPO_PRODUTO"]:
                sim += 0.25
        if pd.notna(linha26) and pd.notna(row_h["LINHA"]):
            if linha26 == row_h["LINHA"]:
                sim += 0.20
        if sim > 0:
            sim_scores.append((row_h["PRODUTO"], row_h["COR_PRODUTO"], sim))

    if not sim_scores:
        for filial in TARGET_STORES:
            results.append({
                "PRODUTO": produto, "COR_PRODUTO": cor, "FILIAL": filial,
                "velocidade_prevista": vel_media_filial.get(filial, 0),
                "n_similares": 0, "sim_media": 0.0, "metodo": "fallback_sem_similares"
            })
        continue

    # Top-K
    sim_scores.sort(key=lambda x: x[2], reverse=True)
    top_k = sim_scores[:K_NEIGHBORS]
    top_k_df = pd.DataFrame(top_k, columns=["PRODUTO_HIST", "COR_PRODUTO_HIST", "SIM"])

    # Para cada filial, calcular velocidade ponderada
    for filial in TARGET_STORES:
        vel_filial = vel_hist[vel_hist["filial_canon"] == filial].copy()

        if vel_filial.empty:
            vel_pred = vel_media_filial.get(filial, 0)
            metodo = "fallback_filial_vazia"
        else:
            # Juntar com os top-K similares
            matched = top_k_df.merge(
                vel_filial[["PRODUTO", "COR_PRODUTO", "velocidade_dia"]],
                left_on=["PRODUTO_HIST", "COR_PRODUTO_HIST"],
                right_on=["PRODUTO", "COR_PRODUTO"],
                how="inner"
            )

            if matched.empty or matched["velocidade_dia"].sum() == 0:
                # Fallback: média da categoria na filial
                vel_cat = vel_filial[vel_filial["GRUPO_PRODUTO"] == grupo26]["velocidade_dia"]
                vel_pred = vel_cat[vel_cat > 0].median() if (vel_cat > 0).any() else vel_media_filial.get(filial, 0)
                metodo = "fallback_categoria"
            else:
                # Média ponderada pela similaridade
                total_sim = matched["SIM"].sum()
                vel_pred  = (matched["velocidade_dia"] * matched["SIM"]).sum() / total_sim
                metodo = "knn_ponderado"

        results.append({
            "PRODUTO": produto, "COR_PRODUTO": cor, "FILIAL": filial,
            "velocidade_prevista": round(vel_pred, 6),
            "n_similares": len(top_k),
            "sim_media": round(sum(s[2] for s in top_k) / len(top_k), 3),
            "metodo": metodo
        })

df_vel = pd.DataFrame(results)

print(f"\n=== VELOCIDADES PREVISTAS ===")
print(f"Total linhas: {len(df_vel)}")
print(f"Método de cálculo:")
print(df_vel["metodo"].value_counts().to_string())
print(f"\nVelocidade prevista mediana: {df_vel['velocidade_prevista'].median():.4f} pcs/dia")
print(f"Velocidade prevista máxima: {df_vel['velocidade_prevista'].max():.4f} pcs/dia")
print(f"\nVelocidade média prevista por filial:")
print(df_vel.groupby("FILIAL")["velocidade_prevista"].mean().sort_values(ascending=False).to_string())

# ─── 6. Calcular demanda prevista no horizonte (14 + leadtime) ───────────────

# Merge com leadtimes
df_vel = df_vel.merge(leadtimes, on="FILIAL", how="left")
df_vel["horizonte_dias"]    = 14 + df_vel["LEADTIME"]
df_vel["demanda_prevista"]  = df_vel["velocidade_prevista"] * df_vel["horizonte_dias"]
df_vel["demanda_arredondada"] = df_vel["demanda_prevista"].apply(lambda x: max(1, round(x)) if x > 0.5 else 0)

print(f"\nDemanda prevista total por filial (unidades):")
resumo = df_vel.groupby("FILIAL").agg(
    demanda_total = ("demanda_arredondada", "sum"),
    horizonte     = ("horizonte_dias", "first"),
    produtos      = ("PRODUTO", "nunique")
).sort_values("demanda_total", ascending=False)
print(resumo.to_string())

# ─── 7. Salvar resultado ──────────────────────────────────────────────────────

output_path = BASE / "velocidade_prevista_inv26.csv"
df_vel.to_csv(output_path, index=False)
print(f"\nResultado salvo em: {output_path}")
print(f"Colunas: {list(df_vel.columns)}")
print("\nPrimeiras 5 linhas:")
print(df_vel.head().to_string())
