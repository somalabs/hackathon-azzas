"""
Gera app/data.js — payload embarcado para o SPA de distribuição (Fábula INV26, v3).
Lê o output do algoritmo (distribuicao_inv26.csv) + inputs + velocidade v3 e
produz todas as agregações que os dashboards precisam. Sem PII, dados agregados.
"""
import pandas as pd, numpy as np, json
from pathlib import Path

BASE = Path("C:/Users/IIA/Documents/hackathon-azzas")
TAM_COLS = ["TAM_1","TAM_2","TAM_3","TAM_4","TAM_5","TAM_6"]

compra    = pd.read_excel(BASE/"docs/pilares/compras-dados/compra_INV26_lancamento_fabula.xlsx")
sort_raw  = pd.read_excel(BASE/"docs/pilares/compras-dados/sortimento_INV26_lancamento_fabula.xlsx")
leadtimes = pd.read_excel(BASE/"docs/pilares/compras-dados/leadtimes_INV26_lancamento_fabula.xlsx")
vel       = pd.read_csv(BASE/"velocidade_prevista_inv26_v4.csv")
dist      = pd.read_csv(BASE/"distribuicao_inv26.csv")

for df in (compra, sort_raw, vel):
    df["PRODUTO"] = df["PRODUTO"].astype(float)
compra["COR_PRODUTO"]  = compra["COR_PRODUTO"].astype(int)
sort_raw["COR_PRODUTO"]= sort_raw["COR_PRODUTO"].astype(int)
vel["COR_PRODUTO"]     = vel["COR_PRODUTO"].astype(int)
dist["PRODUTO"]        = dist["PRODUTO"].astype(float)
dist["COR_PRODUTO"]    = dist["COR_PRODUTO"].astype(int)

# desc lookup
desc_map = {}
if "DESCRICAO" in compra.columns:
    for _, r in compra.iterrows():
        desc_map[(r["PRODUTO"], int(r["COR_PRODUTO"]))] = str(r["DESCRICAO"])

attrs = pd.read_csv(BASE/"produtos_inv26_attrs.csv")
attrs["PRODUTO"] = attrs["PRODUTO"].astype(float)
grupo_map = dict(zip(attrs["PRODUTO"], attrs.get("GRUPO_PRODUTO", pd.Series(dtype=str))))

total_comprado = int(compra["COMPRA"].sum())
total_distrib  = int(dist["QTD_DISTRIBUIR"].sum())

# ── META ──────────────────────────────────────────────────────────────────
meta = {
    "colecao": "INV26", "marca": "Fábula", "canal": "Varejo físico (VENDA_LOJA)",
    "versao_algoritmo": "v4", "data_base_modelo": "2026-03-31",
    "n_filiais": int(dist["FILIAL"].nunique()),
    "n_produto_cor": int(len(compra)),
    "total_comprado": total_comprado,
    "total_distribuido": total_distrib,
    "sobra_cd": total_comprado - total_distrib,
    "pct_distribuido": round(total_distrib/total_comprado*100, 1),
    "n_linhas_output": int(len(dist)),
    "metodo_demanda": str(vel["metodo"].mode()[0]) if "metodo" in vel.columns else "knn_enriquecido",
}

# ── CRITÉRIOS ────────────────────────────────────────────────────────────
criterios = {
    "dimensoes": [
        {"nome":"GRUPO_PRODUTO","label":"Tipo de peça","peso":0.35},
        {"nome":"PRECO","label":"Faixa de preço","peso":0.15},
        {"nome":"TECIDO","label":"Família de tecido","peso":0.15},
        {"nome":"PRAIA_BEBE","label":"Flag praia + bebê","peso":0.15},
        {"nome":"MANGA","label":"Estilo de manga","peso":0.10},
        {"nome":"ESTAMPA","label":"Estampado vs liso","peso":0.10},
    ],
    "pesos_colecao": {"INV23":1.0,"INV24":2.0,"INV25":3.0},
    "faixas_preco": [
        {"tier":"T1","label":"< R$100"},{"tier":"T2","label":"R$100–199"},
        {"tier":"T3","label":"R$200–299"},{"tier":"T4","label":"≥ R$300"}],
    "janela_on_season_dias": 122,
    "regras": {
        "horizonte": "14 + leadtime (dias)",
        "limiar_grade": "≥ 50% dos tamanhos ativos com ≥ 1 un.",
        "min_un_sku": 1,
        "prioridade_falta_estoque": "leadtime decrescente (lojas distantes primeiro)",
        "sortimento": "SORTIMENTO = NÃO → 0 unidades",
    },
}

# ── FILIAIS ──────────────────────────────────────────────────────────────
lt_map = dict(zip(leadtimes["FILIAL"], leadtimes["LEADTIME"]))
vel_f = vel.groupby("FILIAL").agg(
    vel_media=("velocidade_prevista","mean"),
    demanda_prevista=("demanda_arredondada","sum"),
    leadtime=("LEADTIME","max"),
    horizonte=("horizonte_dias","max"),
).reset_index()
dist_f = dist.groupby("FILIAL").agg(qtd_recebida=("QTD_DISTRIBUIR","sum")).reset_index()
npc_f  = dist.groupby("FILIAL").apply(
    lambda g: g[["PRODUTO","COR_PRODUTO"]].drop_duplicates().shape[0]).rename("n_produto_cor").reset_index()

filiais = []
for _, r in vel_f.iterrows():
    f = r["FILIAL"]
    receb = int(dist_f.loc[dist_f["FILIAL"]==f,"qtd_recebida"].sum()) if f in dist_f["FILIAL"].values else 0
    npc   = int(npc_f.loc[npc_f["FILIAL"]==f,"n_produto_cor"].sum()) if f in npc_f["FILIAL"].values else 0
    dem   = int(r["demanda_prevista"])
    filiais.append({
        "filial": f.replace("FABULA ","").strip(),
        "filial_full": f,
        "leadtime": int(r["leadtime"]),
        "horizonte": int(r["horizonte"]),
        "vel_media": round(float(r["vel_media"]),3),
        "demanda_prevista": dem,
        "qtd_recebida": receb,
        "pct_atendido": round(receb/dem*100,1) if dem>0 else 0.0,
        "n_produto_cor": npc,
    })
filiais.sort(key=lambda x: x["qtd_recebida"], reverse=True)

# ── PRODUTOS (produto-cor) ───────────────────────────────────────────────
dist_pc = dist.groupby(["PRODUTO","COR_PRODUTO"]).agg(
    distribuido=("QTD_DISTRIBUIR","sum"),
    n_filiais=("FILIAL","nunique")).reset_index()
produtos = []
for _, r in compra.iterrows():
    p, c = r["PRODUTO"], int(r["COR_PRODUTO"])
    comp = int(r["COMPRA"])
    drow = dist_pc[(dist_pc["PRODUTO"]==p)&(dist_pc["COR_PRODUTO"]==c)]
    distr = int(drow["distribuido"].iloc[0]) if len(drow) else 0
    nf    = int(drow["n_filiais"].iloc[0]) if len(drow) else 0
    grade = {t:int(r[t]) for t in TAM_COLS if t in compra.columns and int(r[t])>0}
    produtos.append({
        "produto": f"{p:.5f}".rstrip("0").rstrip("."),
        "cor": c,
        "desc": desc_map.get((p,c),""),
        "grupo": str(grupo_map.get(p,"")) if pd.notna(grupo_map.get(p,"")) else "",
        "comprado": comp, "distribuido": distr, "sobra_cd": comp-distr,
        "n_filiais": nf, "grade": grade,
    })
produtos.sort(key=lambda x: x["distribuido"], reverse=True)

# por grupo
grp = {}
for pr in produtos:
    g = pr["grupo"] or "(sem grupo)"
    grp.setdefault(g, {"grupo":g,"comprado":0,"distribuido":0,"n_produto_cor":0})
    grp[g]["comprado"]    += pr["comprado"]
    grp[g]["distribuido"] += pr["distribuido"]
    grp[g]["n_produto_cor"]+=1
grupos = sorted(grp.values(), key=lambda x:x["distribuido"], reverse=True)

# ── VALIDAÇÕES ───────────────────────────────────────────────────────────
sort_nao = set(zip(sort_raw[sort_raw["SORTIMENTO"]!="SIM"]["FILIAL"],
                   sort_raw[sort_raw["SORTIMENTO"]!="SIM"]["PRODUTO"],
                   sort_raw[sort_raw["SORTIMENTO"]!="SIM"]["COR_PRODUTO"]))
viol_sort = int(dist.apply(lambda r:(r["FILIAL"],r["PRODUTO"],r["COR_PRODUTO"]) in sort_nao,axis=1).sum())
dist["tam_col"]="TAM_"+dist["TAMANHO"].astype(str)
soma = dist.groupby(["PRODUTO","COR_PRODUTO","tam_col"])["QTD_DISTRIBUIR"].sum().reset_index()
cm = compra.melt(id_vars=["PRODUTO","COR_PRODUTO"],value_vars=TAM_COLS,var_name="tam_col",value_name="disp")
chk = soma.merge(cm,on=["PRODUTO","COR_PRODUTO","tam_col"],how="left")
viol_est = int((chk["QTD_DISTRIBUIR"]>chk["disp"]).sum())
nao_int  = int((dist["QTD_DISTRIBUIR"]<1).sum())
ecomm = int(dist["FILIAL"].isin(["FABULA ECOMMERCE CM","FABULA ECOMMERCE SP CM"]).sum())
n_nao = int((sort_raw["SORTIMENTO"]!="SIM").sum())
validacoes = {
    "checks":[
        {"nome":"Violações de sortimento","valor":viol_sort,"ok":viol_sort==0,"detalhe":f"{n_nao} restrições NÃO respeitadas"},
        {"nome":"Violações de estoque","valor":viol_est,"ok":viol_est==0,"detalhe":"soma ≤ TAM_N comprado"},
        {"nome":"Valores não-inteiros / < 1","valor":nao_int,"ok":nao_int==0,"detalhe":"todas as qtds inteiras ≥ 1"},
        {"nome":"Linhas de e-commerce","valor":ecomm,"ok":ecomm==0,"detalhe":"e-commerce fora de escopo"},
    ],
    "qtd_min": int(dist["QTD_DISTRIBUIR"].min()),
    "qtd_max": int(dist["QTD_DISTRIBUIR"].max()),
}
validacoes["tudo_ok"] = all(c["ok"] for c in validacoes["checks"])

# ── DISTRIBUIÇÃO (tabela completa) ───────────────────────────────────────
distribuicao = [{
    "filial": r["FILIAL"].replace("FABULA ","").strip(),
    "produto": f'{r["PRODUTO"]:.5f}'.rstrip("0").rstrip("."),
    "cor": int(r["COR_PRODUTO"]), "tamanho": int(r["TAMANHO"]),
    "qtd": int(r["QTD_DISTRIBUIR"]),
} for _, r in dist.iterrows()]

payload = {"meta":meta,"criterios":criterios,"filiais":filiais,
           "produtos":produtos,"grupos":grupos,"validacoes":validacoes,
           "distribuicao":distribuicao}

(BASE/"app").mkdir(exist_ok=True)
out = BASE/"app/data.js"
out.write_text("window.APP_DATA = "+json.dumps(payload,ensure_ascii=False)+";",encoding="utf-8")
print("OK ->", out)
print(f"meta: {meta['total_distribuido']} distrib / {meta['total_comprado']} comprado "
      f"({meta['pct_distribuido']}%), {len(distribuicao)} linhas, "
      f"{len(produtos)} produto-cor, {len(filiais)} filiais")
print("validações tudo_ok =", validacoes["tudo_ok"])
