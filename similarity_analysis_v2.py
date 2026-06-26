"""
Análise de Similaridade INV26 v2 — Fábula
Modelo enriquecido: GRUPO, SUBGRUPO, fabric_family, is_estampado,
                    preco_tier, is_beach, is_bebe
Data-base: 31/03/2026  |  Canal: Varejo físico  |  Marca: Fábula
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path("C:/Users/IIA/Documents/hackathon-azzas")

# ─── 1. Carregar dados ────────────────────────────────────────────────────────
compra       = pd.read_excel(BASE / "docs/pilares/compras-dados/compra_INV26_lancamento_fabula.xlsx")
sortimento   = pd.read_excel(BASE / "docs/pilares/compras-dados/sortimento_INV26_lancamento_fabula.xlsx")
leadtimes    = pd.read_excel(BASE / "docs/pilares/compras-dados/leadtimes_INV26_lancamento_fabula.xlsx")
attrs_inv26  = pd.read_csv(BASE / "produtos_inv26_attrs.csv")
hist_vendas  = pd.read_csv(BASE / "historico_inv_vendas.csv")
hist_attrs   = pd.read_csv(BASE / "historico_attrs_precos.csv")

# INV26 preços (coletados inline da query BQ)
precos_inv26_raw = [
    ("5.21225",229,114.5,42.07),("5.21231",139,139,26.89),("5.20559",269,134.5,56.39),
    ("5.21194",229,114.5,40.48),("5.20924",149,74.5,26.46),("5.21177",239,239,52.01),
    ("5.21207",259,259,47.07),("5.20788",219,109.5,37.24),("5.20978",279,139.5,59.06),
    ("5.20613",498,498,92.4),("5.20562",298,149,57.91),("5.20825",169,84.5,32.22),
    ("5.20692",339,169.5,58.81),("5.20703",259,129.5,53.26),("5.20829",229,229,47.41),
    ("5.20967",249,249,55.39),("5.21762",119,119,23.27),("5.20792",198,99,38.41),
    ("5.21199",249,249,47.73),("5.20653",229,114.5,40.76),("5.21196",229,114.5,50.51),
    ("5.21157",589,589,130.91),("5.21191",219,219,30.12),("5.21193",229,114.5,47.82),
    ("5.20739",249,124.5,43.89),("5.20758",269,134.5,37.09),("5.20884",169,84.5,31.7),
    ("5.21061",198,99,37.74),("5.21052",129,64.5,23.3),("5.21211",259,129.5,50.09),
    ("5.20588",249,124.5,39.05),("5.21075",179,89.5,37.77),("5.21142",149,74.5,28.5),
    ("5.20575",219,109.5,41.86),("5.21008",239,119.5,44.62),("5.20707",269,134.5,53.32),
    ("5.21665",239,119.5,37.46),("5.21767",279,139.5,32.01),("5.20614",659,329.5,118.63),
    ("5.21236",298,298,73.85),("5.21229",349,349,65.8),("5.21048",139,69.5,25.84),
    ("5.20906",139,69.5,24.75),("5.21051",129,64.5,23.24),("5.20695",229,114.5,46.06),
    ("5.20908",149,74.5,25.74),("5.20841",169,84.5,31.97),("5.20586",169,84.5,33.45),
    ("5.20879",169,84.5,29.47),("5.20747",198,99,36.43),("5.20797",219,109.5,40.0),
    ("5.20971",179,89.5,27.21),("5.20563",279,139.5,55.21),("5.21078",129,129,22.82),
    ("5.20998",149,149,31.22),("5.20701",249,124.5,62.89),("5.20973",239,119.5,50.98),
    ("5.20642",269,134.5,36.33),("5.21195",269,134.5,45.31),("5.20655",569,569,104.14),
    ("5.20965",198,99,42.57),("5.21178",289,289,66.84),("5.20883",169,84.5,30.27),
    ("5.20819",169,84.5,32.47),("5.21224",239,119.5,41.83),("5.20645",198,99,33.89),
    ("5.20954",198,99,36.44),("5.21666",198,198,43.4),("5.20793",189,94.5,36.61),
    ("5.20931",198,99,34.98),("5.20933",239,119.5,44.9),("5.21179",198,198,32.59),
    ("5.21214",169,84.5,34.77),("5.20826",139,69.5,20.3),("5.21163",198,99,40.44),
    ("5.21047",129,64.5,23.14),("5.20877",169,84.5,29.05),("5.20738",249,124.5,52.65),
    ("5.21238",279,279,53.08),("5.20968",249,124.5,47.13),("5.20649",139,69.5,22.04),
    ("5.20972",219,109.5,35.41),("5.21245",139,69.5,20.82),("5.20936",239,119.5,44.35),
    ("5.20807",229,114.5,42.97),("5.20769",129,64.5,23.67),("5.21244",98,98,20.16),
    ("5.21668",289,289,53.46),("5.20657",269,134.5,50.14),("5.21644",179,89.5,37.4),
    ("5.20553",279,139.5,55.69),("5.21021",129,129,25.53),("5.21206",298,298,40.15),
    ("5.20887",169,84.5,29.93),("5.20696",449,224.5,84.25),("5.20911",139,69.5,24.73),
    ("5.20609",159,79.5,23.19),("5.20676",229,114.5,48.18),("5.21176",289,289,57.92),
    ("5.20831",329,329,70.62),("5.20958",198,99,38.84),("5.20944",198,99,35.37),
    ("5.20742",259,129.5,45.79),("5.21182",249,249,49.51),("5.20763",129,64.5,27.6),
    ("5.20785",189,94.5,36.1),("5.20682",269,134.5,53.86),("5.20771",169,84.5,35.97),
    ("5.21667",289,289,60.16),("5.21198",189,94.5,36.4),("5.20787",229,114.5,42.88),
    ("5.20557",219,109.5,44.35),("5.21056",139,69.5,22.8),("5.21162",169,84.5,38.59),
    ("5.20686",289,144.5,57.37),("5.20606",298,298,65.79),("5.20866",169,169,33.23),
    ("5.21226",169,84.5,32.26),("5.21219",198,99,37.54),("5.20578",169,84.5,29.77),
    ("5.21287",398,398,51.31),("5.20805",319,159.5,60.45),("5.20706",398,199,82.06),
    ("5.20959",219,109.5,39.09),("5.21239",198,99,37.6),("5.21286",219,219,44.81),
    ("5.21425",198,198,33.56),("5.21215",119,59.5,26.64),("5.20552",219,109.5,43.67),
    ("5.20979",189,94.5,41.42),("5.20815",169,84.5,32.64),("5.21664",239,119.5,52.11),
    ("5.21143",229,114.5,48.06),("5.20854",249,249,49.54),("5.21766",269,269,56.84),
    ("5.20934",239,119.5,39.0),("5.21227",159,79.5,31.02),("5.20948",129,64.5,27.42),
    ("5.21641",169,84.5,33.34),("5.20596",349,174.5,65.29),("5.21426",198,198,34.59),
    ("5.20752",239,119.5,46.75),("5.21055",129,64.5,24.79),("5.20806",349,174.5,77.3),
    ("5.20951",198,99,36.58),("5.20777",179,89.5,32.87),("5.21159",329,329,74.18),
    ("5.20868",129,129,24.82),("5.21158",449,449,100.47),("5.21054",189,94.5,36.48),
    ("5.21222",198,99,37.56),("5.20745",249,124.5,44.3),("5.20637",498,249,90.39),
    ("5.20702",279,139.5,53.36),("5.20755",259,129.5,47.68),("5.20554",239,119.5,47.0),
    ("5.20976",198,99,35.95),("5.20912",139,69.5,24.85),("5.21027",149,74.5,29.53),
    ("5.20851",139,69.5,23.27),("5.20882",198,99,46.73),("5.20694",198,99,44.42),
    ("5.21026",129,64.5,24.03),("5.20828",149,74.5,24.97),("5.20699",269,134.5,51.27),
    ("5.20583",189,94.5,34.2),("5.21634",198,198,39.32),("5.20641",359,179.5,74.37),
    ("5.21167",119,119,23.21),("5.20917",139,69.5,25.64),("5.21181",179,179,35.59),
    ("5.21765",98,98,19.84),("5.21251",169,169,70.06),("5.20558",269,134.5,53.97),
    ("5.21764",119,119,22.94),("5.20947",129,64.5,29.95),("5.20691",298,149,64.01),
    ("5.20564",219,219,41.96),("5.21221",269,134.5,35.96),("5.20778",219,109.5,42.19),
    ("5.20937",279,139.5,53.71),("5.21233",169,84.5,28.52),("5.21635",229,114.5,39.88),
    ("5.20881",189,94.5,41.28),("5.21184",159,159,24.89),("5.20862",169,84.5,32.72),
    ("5.21046",129,64.5,23.14),("5.21237",198,198,46.23),("5.21045",139,69.5,25.64),
    ("5.20689",219,109.5,44.71),("5.21175",229,229,50.68),("5.20798",179,89.5,34.13),
    ("5.21205",249,124.5,44.62),("5.20603",598,598,102.43),("5.21124",279,139.5,53.69),
    ("5.21212",239,119.5,45.64),("5.21019",149,74.5,31.53),("5.21006",179,89.5,33.17),
    ("5.20668",229,114.5,40.33),("5.20704",239,119.5,49.33),("5.20919",249,124.5,41.04),
    ("5.20592",498,249,96.92),("5.21111",229,229,49.7),("5.20658",279,139.5,51.51),
    ("5.20681",298,149,62.54),("5.20576",198,99,36.44),("5.21223",189,94.5,31.26),
    ("5.20969",249,249,46.09),("5.21169",239,119.5,47.56),("5.20878",219,109.5,42.96),
    ("5.21123",98,98,21.21),("5.20616",379,189.5,71.55),("5.20705",279,139.5,58.6),
    ("5.20853",129,64.5,17.78),("5.21168",329,164.5,51.3),("5.20886",179,89.5,39.38),
    ("5.20907",149,74.5,23.91),("5.21633",359,179.5,69.51),("5.20754",239,119.5,39.31),
    ("5.20556",349,174.5,62.12),("5.21139",119,59.5,23.0),("5.21074",189,94.5,38.89),
    ("5.21031",159,79.5,28.63),("5.20974",179,89.5,34.28),("5.20643",298,149,58.78),
    ("5.21106",379,379,77.17),("5.21185",298,149,66.01),("5.20999",179,179,43.66),
    ("5.20651",198,99,40.21),("5.20577",189,94.5,36.53),("5.20693",198,99,43.22),
    ("5.20652",289,289,56.46),("5.21192",198,198,41.26),("5.21643",179,89.5,28.7),
    ("5.21204",249,124.5,46.56),("5.20749",239,119.5,40.06),("5.21242",109,109,21.26),
    ("5.21025",139,69.5,26.03),("5.20964",249,124.5,48.73),("5.21209",259,259,45.93),
    ("5.20927",149,74.5,24.79),("5.21028",119,119,24.84),("5.21424",289,289,58.89),
    ("5.20953",198,99,42.15),("5.20926",149,74.5,24.03),("5.20743",259,129.5,67.02),
    ("5.20776",179,89.5,29.36),("5.21427",249,249,47.97),("5.20697",269,134.5,51.12),
    ("5.20918",339,169.5,64.42),("5.20555",298,149,53.21),("5.21763",119,119,23.3),
]
precos_inv26 = pd.DataFrame(precos_inv26_raw, columns=["PRODUTO","preco_original","preco_varejo","preco_custo"])

print(f"Preços INV26 carregados: {len(precos_inv26)} produtos")

# ─── 2. Funções de feature engineering ──────────────────────────────────────

def parse_fabric_family(linha):
    if pd.isna(linha): return "DESCONHECIDO"
    l = str(linha).upper()
    if "TECIDO PLANO" in l: return "TECIDO_PLANO"
    if "MALHA"        in l: return "MALHA"
    if "MOLETOM"      in l: return "MOLETOM"
    if "SARJA"        in l: return "SARJA"
    if "TRICOT"       in l: return "TRICOT"
    if "LYCRA"        in l: return "LYCRA"
    if "PRAIA"        in l: return "PRAIA"
    if l.startswith("EM") or l in ("EMI","EMB","EMT","ESI"): return "EMB_ESPECIAL"
    if "ACESSORIO"    in l: return "ACESSORIO"
    return "OUTROS"

def parse_is_estampado(linha):
    if pd.isna(linha): return None
    l = str(linha).upper()
    if "ESTAMPADO" in l or "ESTAMPADA" in l: return 1
    if "LISO" in l or "LISA" in l:           return 0
    return None   # PRAIA, SARJA etc. — não classificado

def parse_preco_tier(preco):
    if pd.isna(preco) or preco <= 0: return None
    if preco <  100: return 1   # baixo
    if preco <  200: return 2   # médio
    if preco <  300: return 3   # alto
    return 4                     # premium

def parse_is_beach(linha, grupo):
    l = str(linha).upper() if pd.notna(linha) else ""
    g = str(grupo).upper() if pd.notna(grupo) else ""
    return 1 if ("PRAIA" in l or any(k in g for k in ["BIQUINI","SUNGA","MAIÔ","MAIAO","UV"])) else 0

def parse_is_bebe(desc):
    if pd.isna(desc): return 0
    d = str(desc).upper()
    return 1 if ("BEBE" in d or " MINI" in d or "INFANTIL" in d) else 0

def parse_manga(subgrupo):
    if pd.isna(subgrupo): return "DESCONHECIDO"
    s = str(subgrupo).upper()
    if "MANGA CURTA" in s or "MC" in s:  return "MANGA_CURTA"
    if "MANGA LONGA" in s or "ML" in s:  return "MANGA_LONGA"
    if "SEM MANGA"   in s:               return "SEM_MANGA"
    if "REGATA"      in s:               return "SEM_MANGA"
    return "OUTRO"

def enrich(df):
    df = df.copy()
    df["fabric_family"] = df["LINHA"].apply(parse_fabric_family)
    df["is_estampado"]  = df["LINHA"].apply(parse_is_estampado)
    df["preco_tier"]    = df["preco_varejo"].apply(parse_preco_tier)
    df["is_beach"]      = df.apply(lambda r: parse_is_beach(r.get("LINHA"), r.get("GRUPO_PRODUTO")), axis=1)
    df["is_bebe"]       = df["DESC_PRODUTO"].apply(parse_is_bebe) if "DESC_PRODUTO" in df else 0
    df["manga"]         = df["SUBGRUPO_PRODUTO"].apply(parse_manga) if "SUBGRUPO_PRODUTO" in df else "DESCONHECIDO"
    return df

# ─── 3. Enriquecer INV26 ──────────────────────────────────────────────────────
compra["PRODUTO"] = compra["PRODUTO"].astype(str)
attrs_inv26["PRODUTO"] = attrs_inv26["PRODUTO"].astype(str)
precos_inv26["PRODUTO"] = precos_inv26["PRODUTO"].astype(str)

inv26 = (
    compra[["PRODUTO","COR_PRODUTO","DESCRICAO","COMPRA"]]
    .merge(attrs_inv26[["PRODUTO","GRUPO_PRODUTO","SUBGRUPO_PRODUTO","LINHA"]], on="PRODUTO", how="left")
    .merge(precos_inv26[["PRODUTO","preco_varejo","preco_original"]], on="PRODUTO", how="left")
)
inv26 = inv26.rename(columns={"DESCRICAO": "DESC_PRODUTO"})
inv26 = enrich(inv26)

print(f"\nINV26 enriquecido: {len(inv26)} produto-cor")
print("Distribuição preco_tier:", inv26["preco_tier"].value_counts().sort_index().to_dict())
print("Distribuição fabric_family:", inv26["fabric_family"].value_counts().to_dict())
print("is_estampado:", inv26["is_estampado"].value_counts().to_dict())

# ─── 4. Enriquecer histórico ──────────────────────────────────────────────────
hist_attrs["PRODUTO"] = hist_attrs["PRODUTO"].astype(str)
hist_attrs_e = enrich(hist_attrs)

hist_vendas["PRODUTO"] = hist_vendas["PRODUTO"].astype(str)

# Mapa de filial canônica (igual ao v1)
STORE_MAP = {
    "FABULA SHOP LEBLON CM":   ["FABULA SHOP LEBLON CM"],
    "FABULA BARRA SHOPPING":   ["FABULA BARRA SHOPPING","FABULA BARRA SHOP"],
    "FABULA RIO SUL CM":       ["FABULA RIO SUL CM"],
    "FABULA RDB CM":           ["FABULA RDB CM"],
    "FABULA HARMONIA SP CM":   ["FABULA HARMONIA SP CM","FABULA HARMONIA SP"],
    "FABULA PLAZA SHOP CM":    ["FABULA PLAZA SHOP CM","FABULA PLAZA SHOP"],
    "FABULA SHOP VITORIA CM":  ["FABULA SHOP VITORIA CM","FABULA VITORIA CM"],
    "FABULA BARRA SALVADOR CM":["FABULA BARRA SALVADOR CM","FABULA BARRA SALVADOR"],
    "FABULA ELDORADO CM":      ["FABULA ELDORADO CM"],
    "FABULA CENTRO CM":        ["FABULA CENTRO CM"],
}
rev_map = {v: k for k, vs in STORE_MAP.items() for v in vs}
hist_vendas["filial_canon"] = hist_vendas["nome_filial"].map(rev_map)
hist10 = hist_vendas[hist_vendas["filial_canon"].notna()].copy()

ON_DAYS  = {"INV23": 122, "INV24": 122, "INV25": 122}
PESO_COL = {"INV23": 1.0, "INV24": 2.0, "INV25": 3.0}
hist10["on_days"]        = hist10["COLECAO"].map(ON_DAYS)
hist10["peso"]           = hist10["COLECAO"].map(PESO_COL)
hist10["pecas_pos"]      = hist10["pecas_vendidas"].clip(lower=0)
hist10["velocidade_dia"] = hist10["pecas_pos"] / hist10["on_days"]

def weighted_vel(g):
    tp = g["peso"].sum()
    return pd.Series({
        "velocidade_dia":   (g["velocidade_dia"]*g["peso"]).sum()/tp if tp else 0,
        "pecas_total_hist": g["pecas_pos"].sum(),
    })

vel_hist = (
    hist10.groupby(["PRODUTO","COR_PRODUTO","filial_canon"])
    .apply(weighted_vel, include_groups=False)
    .reset_index()
)
# Juntar atributos do histórico (por PRODUTO, sem cor)
vel_hist = vel_hist.merge(
    hist_attrs_e[["PRODUTO","GRUPO_PRODUTO","SUBGRUPO_PRODUTO","LINHA",
                  "fabric_family","is_estampado","preco_tier","is_beach","manga"]].drop_duplicates("PRODUTO"),
    on="PRODUTO", how="left"
)

print(f"\nVel. históricas calculadas: {len(vel_hist)} linhas")
print("Cobertura preco_tier no histórico:", vel_hist["preco_tier"].notna().mean()*100, "%")

# ─── 5. Função de similaridade enriquecida ───────────────────────────────────

WEIGHTS = {
    "GRUPO_PRODUTO":   0.35,
    "manga":           0.10,
    "fabric_family":   0.15,
    "is_estampado":    0.10,
    "preco_tier":      0.15,
    "is_beach":        0.07,
    "is_bebe":         0.08,
}

def similarity(a, b):
    """a = linha INV26, b = linha histórica (dict/Series)"""
    score = 0.0

    # GRUPO_PRODUTO: exact match
    if pd.notna(a.get("GRUPO_PRODUTO")) and pd.notna(b.get("GRUPO_PRODUTO")):
        if a["GRUPO_PRODUTO"] == b["GRUPO_PRODUTO"]:
            score += WEIGHTS["GRUPO_PRODUTO"]

    # manga (sleeve style)
    ma, mb = a.get("manga","DESCONHECIDO"), b.get("manga","DESCONHECIDO")
    if ma != "DESCONHECIDO" and mb != "DESCONHECIDO":
        if ma == mb:
            score += WEIGHTS["manga"]
        elif {ma, mb} == {"MANGA_CURTA", "SEM_MANGA"}:
            score += WEIGHTS["manga"] * 0.4   # parcial

    # fabric_family: exact match
    if a.get("fabric_family","DESCONHECIDO") != "DESCONHECIDO" and \
       b.get("fabric_family","DESCONHECIDO") != "DESCONHECIDO":
        if a["fabric_family"] == b["fabric_family"]:
            score += WEIGHTS["fabric_family"]

    # is_estampado: exact match (só se ambos classificados)
    ea, eb = a.get("is_estampado"), b.get("is_estampado")
    if ea is not None and eb is not None and pd.notna(ea) and pd.notna(eb):
        if int(ea) == int(eb):
            score += WEIGHTS["is_estampado"]

    # preco_tier: exact = full, 1 nível de distância = 0.5, 2+ = 0
    ta, tb = a.get("preco_tier"), b.get("preco_tier")
    if ta is not None and tb is not None and pd.notna(ta) and pd.notna(tb):
        dist = abs(int(ta) - int(tb))
        if   dist == 0: score += WEIGHTS["preco_tier"]
        elif dist == 1: score += WEIGHTS["preco_tier"] * 0.5

    # is_beach
    bea, beb = int(a.get("is_beach", 0) or 0), int(b.get("is_beach", 0) or 0)
    if bea == beb:
        score += WEIGHTS["is_beach"]

    # is_bebe
    iba, ibb = int(a.get("is_bebe", 0) or 0), int(b.get("is_bebe", 0) or 0)
    if iba == ibb:
        score += WEIGHTS["is_bebe"]

    return score

# ─── 6. Calcular velocidade prevista ─────────────────────────────────────────

TARGET_STORES = leadtimes["FILIAL"].tolist()
K = 15

vel_media_filial = (
    vel_hist.groupby("filial_canon")["velocidade_dia"]
    .agg(lambda x: x[x > 0].median() if (x > 0).any() else 0)
    .to_dict()
)

# Pre-indexar histórico por produto único (sem cor, para similaridade de categoria)
hist_uniq = vel_hist.drop_duplicates("PRODUTO")[
    ["PRODUTO","GRUPO_PRODUTO","manga","fabric_family","is_estampado","preco_tier","is_beach"]
].copy()
hist_uniq_dict = hist_uniq.to_dict("records")

results = []
n_total = len(inv26)
print(f"\nProcessando {n_total} produto-cor × {len(TARGET_STORES)} filiais...")

for idx, row26 in inv26.iterrows():
    if idx % 50 == 0:
        print(f"  {idx}/{n_total}")

    produto = str(row26["PRODUTO"])
    cor     = row26["COR_PRODUTO"]
    a       = row26.to_dict()

    # Calcular similaridade com cada produto histórico único
    sims = []
    for h in hist_uniq_dict:
        s = similarity(a, h)
        if s > 0:
            sims.append((h["PRODUTO"], s))

    sims.sort(key=lambda x: x[1], reverse=True)
    top_k = sims[:K]
    top_prods = {p for p, _ in top_k}
    sim_map   = {p: s for p, s in top_k}

    for filial in TARGET_STORES:
        vel_filial = vel_hist[vel_hist["filial_canon"] == filial]

        if vel_filial.empty:
            results.append({"PRODUTO": produto, "COR_PRODUTO": cor, "FILIAL": filial,
                             "velocidade_prevista": vel_media_filial.get(filial, 0),
                             "n_similares": 0, "sim_media": 0.0, "metodo": "fallback_filial_vazia"})
            continue

        if not top_prods:
            grupo = a.get("GRUPO_PRODUTO")
            vel_cat = vel_filial[vel_filial["GRUPO_PRODUTO"] == grupo]["velocidade_dia"] if grupo else pd.Series(dtype=float)
            v = vel_cat[vel_cat > 0].median() if (vel_cat > 0).any() else vel_media_filial.get(filial, 0)
            results.append({"PRODUTO": produto, "COR_PRODUTO": cor, "FILIAL": filial,
                             "velocidade_prevista": v, "n_similares": 0, "sim_media": 0.0, "metodo": "fallback_sem_similares"})
            continue

        matched = vel_filial[vel_filial["PRODUTO"].isin(top_prods)].copy()
        matched["sim"] = matched["PRODUTO"].map(sim_map)

        if matched.empty or matched["velocidade_dia"].sum() == 0:
            grupo = a.get("GRUPO_PRODUTO")
            vel_cat = vel_filial[vel_filial["GRUPO_PRODUTO"] == grupo]["velocidade_dia"] if grupo else pd.Series(dtype=float)
            v = vel_cat[vel_cat > 0].median() if (vel_cat > 0).any() else vel_media_filial.get(filial, 0)
            metodo = "fallback_categoria"
        else:
            total_sim = matched["sim"].sum()
            v = (matched["velocidade_dia"] * matched["sim"]).sum() / total_sim
            metodo = "knn_enriquecido"

        results.append({
            "PRODUTO": produto, "COR_PRODUTO": cor, "FILIAL": filial,
            "velocidade_prevista": round(v, 6),
            "n_similares": len(top_k),
            "sim_media": round(sum(s for _, s in top_k) / len(top_k), 3),
            "metodo": metodo
        })

df_vel = pd.DataFrame(results)

# ─── 7. Métricas & output ─────────────────────────────────────────────────────
df_vel = df_vel.merge(leadtimes, on="FILIAL", how="left")
df_vel["horizonte_dias"]      = 14 + df_vel["LEADTIME"]
df_vel["demanda_prevista"]    = df_vel["velocidade_prevista"] * df_vel["horizonte_dias"]
df_vel["demanda_arredondada"] = df_vel["demanda_prevista"].apply(lambda x: max(1, round(x)) if x > 0.5 else 0)

print("\n=== RESULTADO v2 ===")
print("Método de cálculo:")
print(df_vel["metodo"].value_counts().to_string())
print(f"\nVelocidade mediana: {df_vel['velocidade_prevista'].median():.4f} pcs/dia")
print(f"\nDemanda por filial (horizonte alvo):")
resumo = df_vel.groupby("FILIAL").agg(
    demanda_total     = ("demanda_arredondada","sum"),
    horizonte_dias    = ("horizonte_dias","first"),
    vel_media         = ("velocidade_prevista","mean"),
).sort_values("demanda_total", ascending=False)
resumo["vel_media"] = resumo["vel_media"].round(4)
print(resumo.to_string())

out = BASE / "velocidade_prevista_inv26_v2.csv"
df_vel.to_csv(out, index=False)
print(f"\nSalvo: {out}")

# ─── 8. Comparar v1 vs v2 ────────────────────────────────────────────────────
v1 = pd.read_csv(BASE / "velocidade_prevista_inv26.csv")
comp = (
    df_vel.groupby("FILIAL")["velocidade_prevista"].mean()
    .rename("v2")
    .to_frame()
    .join(v1.groupby("FILIAL")["velocidade_prevista"].mean().rename("v1"))
)
comp["delta_pct"] = ((comp["v2"] - comp["v1"]) / comp["v1"].replace(0, np.nan) * 100).round(1)
print("\n=== Comparação v1 → v2 (velocidade média por filial) ===")
print(comp.sort_values("delta_pct", ascending=False).to_string())
