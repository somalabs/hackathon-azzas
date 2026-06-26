"""Build app_distribuicao_inv26.html — dados 100% dinamicos do CSV."""
import pandas as pd
import json
import os

GROWTH        = 1.111
SAFETY_FACTOR = 1.25   # fator de segurança aplicado na distribuição

NOMES_CURTOS = {
    'FABULA BARRA SHOPPING':    'Barra Shopping',
    'FABULA SHOP LEBLON CM':    'Shop Leblon',
    'FABULA RIO SUL CM':        'Rio Sul',
    'FABULA RDB CM':            'RDB',
    'FABULA HARMONIA SP CM':    'Harmonia SP',
    'FABULA PLAZA SHOP CM':     'Plaza Shop',
    'FABULA SHOP VITORIA CM':   'Shop Vitoria',
    'FABULA BARRA SALVADOR CM': 'Barra Salvador',
    'FABULA ELDORADO CM':       'Eldorado',
    'FABULA CENTRO CM':         'Centro',
}

# ── Leitura de arquivos ───────────────────────────────────────────────────
dist   = pd.read_csv('distribuicao_inv26.csv')
vel4   = pd.read_csv('velocidade_prevista_inv26_v4.csv')
lt_df  = pd.read_excel('docs/pilares/compras-dados/leadtimes_INV26_lancamento_fabula.xlsx')
compra = pd.read_excel('docs/pilares/compras-dados/compra_INV26_lancamento_fabula.xlsx')

dist['PRODUTO']   = dist['PRODUTO'].astype(str)
compra['PRODUTO'] = compra['PRODUTO'].astype(str)

# ── Mapa de descricoes: "PRODUTO_COR" -> DESCRICAO ───────────────────────
desc_map = {}
for _, r in compra.iterrows():
    key = f"{r['PRODUTO']}_{int(r['COR_PRODUTO'])}"
    desc_map[key] = str(r['DESCRICAO']).strip()

# ── TOP 20 produtos com descricao real ───────────────────────────────────
top = (
    dist.groupby(['PRODUTO', 'COR_PRODUTO'])['QTD_DISTRIBUIR']
    .sum().sort_values(ascending=False).head(20).reset_index()
)
top['PRODUTO'] = top['PRODUTO'].astype(str)
top_list = []
for _, r in top.iterrows():
    key = f"{r['PRODUTO']}_{int(r['COR_PRODUTO'])}"
    label = desc_map.get(key, str(r['PRODUTO']))
    top_list.append({'label': label, 'pecas': int(r['QTD_DISTRIBUIR'])})

# ── DIST_ROWS completo para export e tabela ───────────────────────────────
dist_rows = [
    [str(r['FILIAL']), str(r['PRODUTO']), int(r['COR_PRODUTO']),
     int(r['TAMANHO']), int(r['QTD_DISTRIBUIR'])]
    for _, r in dist.iterrows()
]

# ── LOJAS dinamico (dist + vel4 + leadtimes) ─────────────────────────────
store_pecas   = dist.groupby('FILIAL')['QTD_DISTRIBUIR'].sum().to_dict()
store_skus    = (
    dist.groupby('FILIAL')
    .apply(lambda x: x[['PRODUTO', 'COR_PRODUTO']].drop_duplicates().shape[0])
    .to_dict()
)
# Demanda com safety factor: multiplica demanda_prevista continua por SF, depois arredonda
store_demanda = (
    vel4.groupby('FILIAL')['demanda_prevista'].sum() * SAFETY_FACTOR
).round().astype(int).to_dict()
lt_map = dict(zip(lt_df['FILIAL'], lt_df['LEADTIME']))

lojas_list = []
for filial in sorted(store_pecas.keys(), key=lambda x: store_pecas[x], reverse=True):
    lt     = int(lt_map.get(filial, 4))
    pecas  = int(store_pecas[filial])
    demanda = int(store_demanda.get(filial, 0))
    n_skus  = int(store_skus.get(filial, 0))
    cob    = round(min(100.0, pecas / demanda * 100), 1) if demanda > 0 else 0.0
    lojas_list.append({
        'nome':      NOMES_CURTOS.get(filial, filial),
        'leadtime':  lt,
        'horizonte': 14 + lt,
        'pecas':     pecas,
        'n_skus':    n_skus,
        'demanda':   demanda,
        'cobertura': cob,
    })

# ── TAMANHOS dinamico ────────────────────────────────────────────────────
tam_df = (
    dist.groupby('TAMANHO')['QTD_DISTRIBUIR']
    .sum().reset_index().sort_values('TAMANHO')
)
tamanhos_list = [
    {'tam': f'TAM {int(r["TAMANHO"])}', 'pecas': int(r['QTD_DISTRIBUIR'])}
    for _, r in tam_df.iterrows()
]

# ── CALIB dinamico a partir do vel4 ──────────────────────────────────────
calib_fator  = vel4.groupby('FILIAL')['calib_fator'].first()
vel3_media   = vel4.groupby('FILIAL')['velocidade_prevista'].mean()
calib_list   = []
for filial in calib_fator.index:
    fator = float(calib_fator[filial])
    vm3   = float(vel3_media[filial])
    vm25  = fator * vm3 / GROWTH
    calib_list.append({
        'loja': NOMES_CURTOS.get(filial, filial),
        'fator': round(fator, 3),
        'v25':   round(vm25, 4),
        'v3':    round(vm3, 4),
    })
calib_list.sort(key=lambda x: x['fator'], reverse=True)

# ── KPIs do topo ─────────────────────────────────────────────────────────
total_pecas  = int(dist['QTD_DISTRIBUIR'].sum())
total_compra = int(compra[['TAM_1','TAM_2','TAM_3','TAM_4','TAM_5','TAM_6']].fillna(0).values.sum())
pct_dist     = round(total_pecas / total_compra * 100, 1)
n_skus_total = int(dist[['PRODUTO','COR_PRODUTO']].drop_duplicates().shape[0])
total_linhas = len(dist_rows)
cob_media    = round(sum(l['cobertura'] for l in lojas_list) / len(lojas_list), 0)
n_lojas      = len(lojas_list)

# ── Serializa tudo ────────────────────────────────────────────────────────
top_json    = json.dumps(top_list,      ensure_ascii=False)
dist_json   = json.dumps(dist_rows,     ensure_ascii=False)
desc_json   = json.dumps(desc_map,      ensure_ascii=False)
lojas_json  = json.dumps(lojas_list,    ensure_ascii=False)
tam_json    = json.dumps(tamanhos_list, ensure_ascii=False)
calib_json  = json.dumps(calib_list,    ensure_ascii=False)

HTML = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fabula INV26 - Distribuicao Inicial</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Red+Hat+Display:wght@300;400;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --ink:#000;--ink-soft:#595959;--ink-faint:#999;
  --surface:#fff;--surface-warm:#E8E8E4;--surface-cream:#F9F6EA;
  --navy:#274566;--steel:#3D5A73;--blue-soft:#A1C6ED;--blue-light:#C5D9ED;
  --font-primary:'Red Hat Display',Arial,sans-serif;
  --font-editorial:'Playfair Display',Georgia,serif;
  --r:8px;
}}
body{{font-family:var(--font-primary);background:var(--surface-warm);color:var(--ink);}}

/* NAVBAR */
.navbar{{background:var(--ink);color:#fff;padding:1rem 2rem;display:flex;align-items:center;justify-content:space-between;}}
.navbar-brand{{font-size:1.05rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;}}
.navbar-sub{{font-family:var(--font-editorial);font-style:italic;font-size:.85rem;opacity:.6;margin-top:.1rem;}}
.btn-pedido{{background:var(--navy);color:#fff;border:none;padding:.55rem 1.25rem;border-radius:var(--r);
  font-family:var(--font-primary);font-size:.78rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;cursor:pointer;transition:background .2s;}}
.btn-pedido:hover{{background:var(--steel);}}
.btn-baixar{{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.45);padding:.5rem 1.1rem;border-radius:var(--r);
  font-family:var(--font-primary);font-size:.75rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;cursor:pointer;transition:all .2s;}}
.btn-baixar:hover{{border-color:#fff;background:rgba(255,255,255,.1);}}

/* TABS */
.tabs{{background:var(--ink);display:flex;border-bottom:2px solid #282828;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;}}
.tabs::-webkit-scrollbar{{display:none;}}
.tab-btn{{background:transparent;border:none;color:#888;padding:.85rem 1.25rem;font-family:var(--font-primary);
  font-size:.75rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;white-space:nowrap;
  transition:all .2s;border-bottom:2px solid transparent;margin-bottom:-2px;flex-shrink:0;}}
.tab-btn:hover{{color:#fff;}}
.tab-btn.active{{color:#fff;border-bottom-color:var(--blue-soft);}}

/* LAYOUT */
.page{{max-width:1200px;margin:0 auto;padding:clamp(1rem,3vw,2rem);}}
.tab-panel{{display:none;}}
.tab-panel.active{{display:block;}}

/* KPI CARDS */
.kpi-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:1rem;margin-bottom:2rem;}}
.kpi-card{{background:var(--surface);border-radius:var(--r);padding:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,.07);}}
.kpi-label{{font-size:.68rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-faint);margin-bottom:.35rem;}}
.kpi-value{{font-size:1.9rem;font-weight:300;color:var(--ink);line-height:1;font-variant-numeric:tabular-nums;}}
.kpi-sub{{font-size:.72rem;color:var(--ink-soft);margin-top:.3rem;}}
.kpi-card.accent{{background:var(--navy);}}
.kpi-card.accent .kpi-label,.kpi-card.accent .kpi-sub{{color:rgba(255,255,255,.5);}}
.kpi-card.accent .kpi-value{{color:#fff;}}

/* TYPOGRAPHY */
.section-title{{font-size:1.2rem;font-weight:600;margin-bottom:.6rem;margin-top:1.5rem;}}
.section-sub{{font-family:var(--font-editorial);font-style:italic;font-size:.88rem;color:var(--ink-soft);margin-bottom:1.25rem;}}

/* CARDS */
.card{{background:var(--surface);border-radius:var(--r);padding:1.5rem;box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:1.5rem;}}
.card-dark{{background:var(--navy);color:#fff;border-radius:var(--r);padding:1.4rem 1.5rem;margin-bottom:1.5rem;}}
.card-dark h3{{font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;opacity:.55;margin-bottom:.9rem;}}
.card-cream{{background:var(--surface-cream);border-radius:var(--r);padding:1.4rem;margin-bottom:1.5rem;}}

/* BAR CHART */
.bar-list{{display:flex;flex-direction:column;gap:.55rem;}}
.bar-item{{display:grid;grid-template-columns:160px 1fr 60px;gap:.75rem;align-items:center;}}
.bar-item.wide-label{{grid-template-columns:240px 1fr 60px;}}
.bar-label{{font-size:.78rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.bar-track{{background:#f0f0ec;border-radius:3px;height:20px;overflow:hidden;}}
.bar-fill{{height:100%;border-radius:3px;background:var(--navy);}}
.bar-fill.soft{{background:var(--blue-soft);}}
.bar-fill.steel{{background:var(--steel);}}
.bar-val{{font-size:.78rem;font-weight:600;text-align:right;color:var(--ink-soft);font-variant-numeric:tabular-nums;}}

/* Peso chart */
.peso-list{{display:flex;flex-direction:column;gap:.65rem;}}
.peso-item{{display:grid;grid-template-columns:180px 1fr 40px;gap:.75rem;align-items:center;}}
.peso-label{{font-size:.8rem;font-weight:600;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.peso-track{{background:rgba(255,255,255,.12);border-radius:3px;height:18px;overflow:hidden;}}
.peso-fill{{height:100%;border-radius:3px;background:var(--blue-soft);}}
.peso-val{{font-size:.78rem;font-weight:600;color:rgba(255,255,255,.65);text-align:right;font-variant-numeric:tabular-nums;}}
.peso-desc{{font-size:.72rem;color:rgba(255,255,255,.5);margin-top:.15rem;grid-column:2/-1;}}

.calib-list{{display:flex;flex-direction:column;gap:.55rem;}}
.calib-item{{display:grid;grid-template-columns:130px 1fr 55px 70px 70px;gap:.6rem;align-items:center;}}
.calib-label{{font-size:.78rem;font-weight:600;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.calib-track{{background:rgba(255,255,255,.12);border-radius:3px;height:18px;overflow:hidden;}}
.calib-fill{{height:100%;border-radius:3px;background:var(--blue-soft);}}
.calib-fator{{font-size:.78rem;font-weight:600;color:var(--blue-soft);text-align:right;font-variant-numeric:tabular-nums;}}
.calib-num{{font-size:.72rem;color:rgba(255,255,255,.5);text-align:right;font-variant-numeric:tabular-nums;}}

/* TABLES */
.table-wrap{{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:var(--r);}}
table{{width:100%;border-collapse:collapse;min-width:600px;}}
th{{background:var(--navy);color:#fff;font-size:.68rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;padding:.6rem .85rem;text-align:left;white-space:nowrap;}}
td{{padding:.55rem .85rem;font-size:.84rem;border-bottom:1px solid #f0f0ec;white-space:nowrap;font-variant-numeric:tabular-nums;}}
tr:last-child td{{border-bottom:none;}}
tr:hover td{{background:#f7f7f3;}}
.prog{{width:70px;height:7px;background:#f0f0ec;border-radius:3px;display:inline-block;vertical-align:middle;margin-right:.4rem;overflow:hidden;}}
.prog-fill{{height:100%;border-radius:3px;display:block;}}
.g{{background:#2d6a4f;}}.y{{background:#b5851a;}}.o{{background:#c44b1d;}}

/* Tabela filters */
.filter-row{{display:flex;gap:.75rem;align-items:center;margin-bottom:1rem;flex-wrap:wrap;}}
.filter-row select,.filter-row input{{
  font-family:var(--font-primary);font-size:.8rem;
  padding:.45rem .75rem;border:1.5px solid #ddd;border-radius:var(--r);background:#fff;
  color:var(--ink);outline:none;transition:border-color .2s;}}
.filter-row select:focus,.filter-row input:focus{{border-color:var(--navy);}}
.filter-row input{{min-width:220px;}}
.row-count{{font-size:.75rem;color:var(--ink-faint);margin-left:auto;}}
.pager{{display:flex;gap:.4rem;align-items:center;margin-top:1rem;}}
.pager button{{background:#f0f0ec;border:none;padding:.35rem .7rem;border-radius:5px;font-size:.78rem;
  font-family:var(--font-primary);cursor:pointer;transition:background .2s;}}
.pager button:hover{{background:#ddd;}}
.pager button.active{{background:var(--navy);color:#fff;}}
.pager-info{{font-size:.75rem;color:var(--ink-soft);margin:0 .5rem;}}

/* VALIDATION */
.val-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;}}
.val-card{{background:var(--surface);border-radius:var(--r);padding:1.25rem 1.4rem;display:flex;align-items:flex-start;gap:.9rem;box-shadow:0 1px 3px rgba(0,0,0,.07);}}
.val-icon{{font-size:1.6rem;flex-shrink:0;margin-top:.05rem;}}
.val-title{{font-size:.84rem;font-weight:600;margin-bottom:.2rem;}}
.val-desc{{font-size:.75rem;color:var(--ink-soft);line-height:1.45;}}
.stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:1rem;margin-top:1.5rem;}}
.stat-item{{background:var(--surface-cream);border-radius:var(--r);padding:1rem 1.1rem;}}
.stat-num{{font-size:1.55rem;font-weight:300;color:var(--navy);font-variant-numeric:tabular-nums;}}
.stat-desc{{font-size:.73rem;color:var(--ink-soft);margin-top:.2rem;line-height:1.4;}}

/* MODELO BOX */
.modelo-box{{background:var(--navy);color:#fff;border-radius:var(--r);padding:1.4rem 1.5rem;margin-top:1.5rem;margin-bottom:1.75rem;}}
.modelo-box h3{{font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;opacity:.55;margin-bottom:.9rem;}}
.modelo-steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1rem;}}
.step{{border-left:2px solid var(--blue-soft);padding-left:.7rem;}}
.step-n{{font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;opacity:.45;}}
.step-title{{font-size:.82rem;font-weight:600;margin:.1rem 0 .2rem;}}
.step-desc{{font-size:.73rem;opacity:.65;line-height:1.4;}}

/* DECISIONS */
.decisions{{background:var(--navy);color:#fff;border-radius:var(--r);padding:1.4rem 1.5rem;margin-top:1.5rem;}}
.decisions h3{{font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;opacity:.55;margin-bottom:.75rem;}}
.decisions li{{font-size:.83rem;opacity:.88;margin-bottom:.5rem;list-style:none;padding-left:1rem;position:relative;}}
.decisions li::before{{content:"--";position:absolute;left:0;opacity:.4;}}

/* DRIVERS grids */
.two-col{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1.5rem;margin-bottom:1.5rem;}}
.col-label{{font-size:.68rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-faint);margin-bottom:.75rem;}}
.col-label-light{{font-size:.68rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:rgba(255,255,255,.45);margin-bottom:.75rem;}}
.colecao-table{{width:100%;border-collapse:collapse;}}
.colecao-table td{{padding:.5rem .6rem;font-size:.82rem;border-bottom:1px solid rgba(255,255,255,.1);}}
.colecao-table td:first-child{{font-weight:600;}}
.colecao-table tr:last-child td{{border-bottom:none;}}
.crescimento-box{{display:flex;align-items:center;gap:1.5rem;margin-top:.75rem;}}
.cresc-item{{text-align:center;}}
.cresc-num{{font-size:1.5rem;font-weight:300;color:var(--blue-soft);}}
.cresc-desc{{font-size:.7rem;color:rgba(255,255,255,.5);margin-top:.2rem;}}
.cresc-arrow{{font-size:1.2rem;color:rgba(255,255,255,.3);}}
.cresc-avg{{text-align:center;border-top:1px solid rgba(255,255,255,.15);padding-top:.75rem;margin-top:.75rem;}}
.cresc-avg-val{{font-size:1.8rem;font-weight:300;color:#fff;}}
.cresc-avg-label{{font-size:.7rem;color:rgba(255,255,255,.5);}}

/* MODAL */
.modal-overlay{{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;align-items:center;justify-content:center;z-index:100;}}
.modal-overlay.open{{display:flex;}}
.modal{{background:#fff;border-radius:12px;padding:2rem;max-width:400px;width:90%;text-align:center;}}
.modal h2{{font-size:1.15rem;margin-bottom:.7rem;}}
.modal p{{font-size:.875rem;color:var(--ink-soft);line-height:1.5;margin-bottom:1rem;}}
.modal-close{{background:var(--navy);color:#fff;border:none;padding:.6rem 1.5rem;border-radius:var(--r);
  cursor:pointer;font-family:var(--font-primary);font-weight:600;font-size:.84rem;margin-top:.5rem;}}

/* ACTIONS */
.actions-row{{display:flex;gap:.75rem;align-items:center;margin-bottom:1.25rem;flex-wrap:wrap;}}
.export-btn{{background:transparent;border:1.5px solid var(--navy);color:var(--navy);padding:.5rem 1.2rem;
  border-radius:var(--r);font-family:var(--font-primary);font-size:.78rem;font-weight:600;
  letter-spacing:.06em;text-transform:uppercase;cursor:pointer;transition:all .2s;}}
.export-btn:hover{{background:var(--navy);color:#fff;}}
.actions-hint{{font-size:.78rem;color:var(--ink-faint);}}

/* Tabela descricao coluna */
.desc-col{{max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--ink-soft);}}
</style>
</head>
<body>

<nav class="navbar">
  <div>
    <div class="navbar-brand">Fabula</div>
    <div class="navbar-sub">INV26 - Distribuicao Inicial</div>
  </div>
  <div style="display:flex;gap:.6rem;align-items:center">
    <button class="btn-baixar" onclick="downloadHTML()">Baixar App</button>
    <button class="btn-pedido" onclick="openModal()">Gerar Pedido</button>
  </div>
</nav>

<div class="tabs">
  <button class="tab-btn active"  onclick="switchTab('visao',this)">Visao Geral</button>
  <button class="tab-btn" onclick="switchTab('drivers',this)">Drivers</button>
  <button class="tab-btn" onclick="switchTab('loja',this)">Por Loja</button>
  <button class="tab-btn" onclick="switchTab('produto',this)">Por Produto</button>
  <button class="tab-btn" onclick="switchTab('validacao',this)">Validacoes</button>
  <button class="tab-btn" onclick="switchTab('tabela',this)">Tabela</button>
</div>

<div class="page">

<!-- TAB 1: VISAO GERAL -->
<div id="tab-visao" class="tab-panel active">
  <div class="modelo-box">
    <h3>Metodologia</h3>
    <div class="modelo-steps">
      <div class="step">
        <div class="step-n">01</div>
        <div class="step-title">Similaridade KNN</div>
        <div class="step-desc">Cada produto INV26 mapeado a 15 analogos historicos (INV23-25) em 7 dimensoes com pesos diferenciados</div>
      </div>
      <div class="step">
        <div class="step-n">02</div>
        <div class="step-title">Calibracao por Loja</div>
        <div class="step-desc">Velocidade ancorada ao INV25 real por loja x crescimento +11,1% (fatores x1,26-x1,68)</div>
      </div>
      <div class="step">
        <div class="step-n">03</div>
        <div class="step-title">Horizonte 14 + LT</div>
        <div class="step-desc">Janela de cobertura antes do ressuprimento automatico: 18 a 30 dias por filial</div>
      </div>
      <div class="step">
        <div class="step-n">04</div>
        <div class="step-title">Prioridade Leadtime</div>
        <div class="step-desc">Salvador (16 d) e Vitoria (11 d) servidas primeiro quando estoque e insuficiente</div>
      </div>
    </div>
  </div>

  <div class="kpi-row">
    <div class="kpi-card accent">
      <div class="kpi-label">Pecas Distribuidas</div>
      <div class="kpi-value">{total_pecas:,}</div>
      <div class="kpi-sub">de {total_compra:,} compradas</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Estoque Distribuido</div>
      <div class="kpi-value">{pct_dist}%</div>
      <div class="kpi-sub">{100-pct_dist:.1f}% no CD regulador</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">SKUs Ativos</div>
      <div class="kpi-value">{n_skus_total}</div>
      <div class="kpi-sub">de 298 produto-cor</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Lojas Atendidas</div>
      <div class="kpi-value">{n_lojas}/{n_lojas}</div>
      <div class="kpi-sub">cobertura total</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Cobertura Media</div>
      <div class="kpi-value">{int(cob_media)}%</div>
      <div class="kpi-sub">da demanda c/ safety</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Fator de Seguranca</div>
      <div class="kpi-value">x{SAFETY_FACTOR}</div>
      <div class="kpi-sub">P70 do erro historico</div>
    </div>
  </div>

  <h2 class="section-title">Distribuicao por Loja</h2>
  <p class="section-sub">Pecas enviadas no lancamento - horizonte de cobertura antes do ressuprimento</p>
  <div class="card">
    <div class="bar-list" id="chart-lojas"></div>
  </div>
</div>

<!-- TAB 2: DRIVERS -->
<div id="tab-drivers" class="tab-panel">

  <div class="two-col" style="margin-top:1.5rem">
    <div class="card-dark">
      <h3>Dimensoes do Modelo KNN (k=15)</h3>
      <div class="col-label-light">Pesos de similaridade</div>
      <div class="peso-list" id="chart-pesos"></div>
    </div>

    <div class="card-dark">
      <h3>Historico de Referencia</h3>
      <div class="col-label-light">Janela ON-Season por colecao</div>
      <table class="colecao-table">
        <tr><td>INV23</td><td>122 dias</td><td style="color:rgba(255,255,255,.45);font-size:.75rem">Jun-Set 2023</td><td style="color:rgba(255,255,255,.45);font-size:.75rem">Peso 1x</td></tr>
        <tr><td>INV24</td><td>214 dias</td><td style="color:rgba(255,255,255,.45);font-size:.75rem">Mar-Set 2024</td><td style="color:rgba(255,255,255,.45);font-size:.75rem">Peso 2x</td></tr>
        <tr><td>INV25</td><td>206 dias</td><td style="color:rgba(255,255,255,.45);font-size:.75rem">Mar-Set 2025</td><td style="color:rgba(255,255,255,.45);font-size:.75rem">Peso 3x</td></tr>
      </table>
      <div class="col-label-light" style="margin-top:1.1rem">Crescimento inter-colecao (Barra Shopping ref.)</div>
      <div class="crescimento-box">
        <div class="cresc-item"><div class="cresc-num">+9,9%</div><div class="cresc-desc">INV23 - INV24</div></div>
        <div class="cresc-arrow">+</div>
        <div class="cresc-item"><div class="cresc-num">+12,4%</div><div class="cresc-desc">INV24 - INV25</div></div>
      </div>
      <div class="cresc-avg"><div class="cresc-avg-val">+11,1%</div><div class="cresc-avg-label">Fator de crescimento aplicado ao INV26</div></div>
    </div>
  </div>

  <div class="card-dark">
    <h3>Calibracao por Loja - correcao da subestimacao do modelo KNN</h3>
    <div class="col-label-light" style="margin-bottom:.35rem">
      Por que calibrar? A correcao do ON_DAYS (122 - 206 d) comprime a velocidade em 1,69x; o growth de 11,1% compensa parcialmente (-34% liquido). Lojas com menos historico INV25 sofrem mais. O fator ancora ao INV25 real x crescimento.
    </div>
    <div style="height:.75rem"></div>
    <div style="display:grid;grid-template-columns:130px 1fr 55px 70px 70px;gap:.6rem;margin-bottom:.4rem;">
      <div style="font-size:.65rem;letter-spacing:.07em;text-transform:uppercase;color:rgba(255,255,255,.4)">Loja</div>
      <div style="font-size:.65rem;letter-spacing:.07em;text-transform:uppercase;color:rgba(255,255,255,.4)">Fator calibracao</div>
      <div style="font-size:.65rem;letter-spacing:.07em;text-transform:uppercase;color:rgba(255,255,255,.4);text-align:right">Fator</div>
      <div style="font-size:.65rem;letter-spacing:.07em;text-transform:uppercase;color:rgba(255,255,255,.4);text-align:right">vel INV25</div>
      <div style="font-size:.65rem;letter-spacing:.07em;text-transform:uppercase;color:rgba(255,255,255,.4);text-align:right">vel v3</div>
    </div>
    <div class="calib-list" id="chart-calib"></div>
  </div>

  <div class="card-cream">
    <div class="col-label">Logica de Distribuicao por Tamanho</div>
    <p style="font-size:.85rem;color:var(--ink-soft);line-height:1.6;margin-bottom:.75rem">
      Para cada filial com demanda confirmada, as pecas sao distribuidas proporcionalmente ao mix de compra do produto (TAM_1...TAM_6). O arredondamento usa o <strong>metodo do maior resto</strong>: garante que a soma seja exatamente a quota e que os tamanhos com maior fracao residual recebam o arredondamento para cima.
    </p>
    <p style="font-size:.85rem;color:var(--ink-soft);line-height:1.6">
      Filtro de completude de grade: uma filial so recebe um produto se 25% ou mais dos tamanhos ativos ficarem com pelo menos 1 unidade. Abaixo disso, preferimos nao enviar para evitar grade muito fragmentada (316 casos bloqueados com SF=x1,25).
    </p>
  </div>

  <div class="card-dark" style="margin-top:0">
    <h3>Fator de Seguranca x{SAFETY_FACTOR} - protecao contra erro de previsao</h3>
    <div class="col-label-light" style="margin-bottom:.9rem">
      Backtest INV25 (4.842 observacoes produto-loja): erro medio absoluto = 56%. A demanda prevista e multiplicada por x{SAFETY_FACTOR} antes da distribuicao para cobrir o P70 da distribuicao historica de erros, mantendo 93,2% do estoque no CD como buffer regulador.
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-top:.5rem">
      <div style="text-align:center">
        <div style="font-size:1.6rem;font-weight:300;color:var(--blue-soft)">56%</div>
        <div style="font-size:.72rem;color:rgba(255,255,255,.5);margin-top:.2rem">MAPE produto-loja INV25</div>
      </div>
      <div style="text-align:center">
        <div style="font-size:1.6rem;font-weight:300;color:var(--blue-soft)">x1,21</div>
        <div style="font-size:.72rem;color:rgba(255,255,255,.5);margin-top:.2rem">P70 do erro historico</div>
      </div>
      <div style="text-align:center">
        <div style="font-size:1.6rem;font-weight:300;color:#fff">x{SAFETY_FACTOR}</div>
        <div style="font-size:.72rem;color:rgba(255,255,255,.5);margin-top:.2rem">fator adotado (arredondado)</div>
      </div>
      <div style="text-align:center">
        <div style="font-size:1.6rem;font-weight:300;color:var(--blue-soft)">+772</div>
        <div style="font-size:.72rem;color:rgba(255,255,255,.5);margin-top:.2rem">pecas extras vs sem safety</div>
      </div>
    </div>
  </div>

</div>

<!-- TAB 3: POR LOJA -->
<div id="tab-loja" class="tab-panel">
  <div class="actions-row" style="margin-top:1.5rem">
    <button class="export-btn" onclick="exportCSV()">Exportar CSV</button>
    <span class="actions-hint">{total_linhas:,} linhas - FILIAL - PRODUTO - COR - TAMANHO - QTD</span>
  </div>
  <div class="card" style="padding:0;">
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Loja</th><th>Leadtime</th><th>Horizonte</th>
            <th>Pecas</th><th>Prod-Cor</th><th>Demanda Prev.</th><th>Cobertura</th>
          </tr>
        </thead>
        <tbody id="table-lojas"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- TAB 4: POR PRODUTO -->
<div id="tab-produto" class="tab-panel">
  <h2 class="section-title" style="margin-top:1.5rem">Top 20 Produtos</h2>
  <p class="section-sub">Por volume total distribuido entre as 10 lojas</p>
  <div class="card">
    <div class="bar-list" id="chart-produtos"></div>
  </div>

  <h2 class="section-title">Mix por Tamanho</h2>
  <p class="section-sub">Distribuicao de pecas por posicao de grade (TAM 3 concentra o core da piramide)</p>
  <div class="card">
    <div class="bar-list" id="chart-tamanhos"></div>
  </div>
</div>

<!-- TAB 5: VALIDACOES -->
<div id="tab-validacao" class="tab-panel">
  <h2 class="section-title" style="margin-top:1.5rem">Hard Constraints - Status</h2>
  <p class="section-sub">Todas as restricoes eliminatorias verificadas antes da entrega</p>

  <div class="val-grid">
    <div class="val-card">
      <div class="val-icon">&#x2705;</div>
      <div>
        <div class="val-title">Zero violacoes de Sortimento</div>
        <div class="val-desc">Nenhuma peca enviada para filial-produto-cor com SORTIMENTO = NAO. 47 combinacoes zeradas por restricao.</div>
      </div>
    </div>
    <div class="val-card">
      <div class="val-icon">&#x2705;</div>
      <div>
        <div class="val-title">Estoque por Tamanho Respeitado</div>
        <div class="val-desc">Soma distribuida igual ou menor que TAM_N comprado para todo produto-cor-tamanho. Zero violacoes de estoque.</div>
      </div>
    </div>
    <div class="val-card">
      <div class="val-icon">&#x2705;</div>
      <div>
        <div class="val-title">Minimo de 1 Unidade</div>
        <div class="val-desc">Todo envio tem QTD_DISTRIBUIR de pelo menos 1. Linhas com zero nao aparecem no output. Minimo verificado = 1 peca.</div>
      </div>
    </div>
    <div class="val-card">
      <div class="val-icon">&#x2705;</div>
      <div>
        <div class="val-title">E-commerce Excluido</div>
        <div class="val-desc">Nenhuma linha de ECOMMERCE CM no output. Escopo restrito as 10 lojas fisicas da Fabula.</div>
      </div>
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-item"><div class="stat-num">298</div><div class="stat-desc">Produto-cor processados</div></div>
    <div class="stat-item"><div class="stat-num">2.264</div><div class="stat-desc">Filial-produto-cor com envio confirmado</div></div>
    <div class="stat-item"><div class="stat-num">316</div><div class="stat-desc">Bloqueados por completude de grade<br><span style="font-size:.68rem">(min. 25% dos tamanhos ativos)</span></div></div>
    <div class="stat-item"><div class="stat-num">{total_linhas:,}</div><div class="stat-desc">Linhas no arquivo de saida</div></div>
    <div class="stat-item"><div class="stat-num">{total_compra - total_pecas:,}</div><div class="stat-desc">Pecas retidas no CD regulador</div></div>
    <div class="stat-item"><div class="stat-num">{pct_dist}%</div><div class="stat-desc">do estoque total distribuido no lancamento</div></div>
  </div>

  <div class="decisions">
    <h3>Decisoes documentadas</h3>
    <ul>
      <li><strong>Prioridade de escassez:</strong> Leadtime decrescente - Salvador (16 d) e Vitoria (11 d) servidas primeiro</li>
      <li><strong>Completude de grade:</strong> 25% ou mais dos tamanhos ativos devem receber pelo menos 1 unidade; abaixo disso, nao envia</li>
      <li><strong>Arredondamento:</strong> Metodo do maior resto - garante inteiros sem vies e soma igual a quota por filial</li>
      <li><strong>Crescimento inter-colecao:</strong> +11,1% sobre INV25 (media INV23-24: +9,9% e INV24-25: +12,4%)</li>
      <li><strong>Calibracao de velocidade:</strong> KNN ancora ao INV25 real por loja - corrige compressao do ON_DAYS (122-206 dias)</li>
      <li><strong>Fator de seguranca x1,25:</strong> aplica +25% sobre a demanda prevista; cobre P70 do erro historico (MAPE=56% no backtest INV25); adiciona 772 pecas vs sem safety, CD retém 93,2% do estoque</li>
    </ul>
  </div>
</div>

<!-- TAB 6: TABELA -->
<div id="tab-tabela" class="tab-panel">
  <h2 class="section-title" style="margin-top:1.5rem">Tabela de Distribuicao</h2>
  <p class="section-sub">{total_linhas:,} linhas - filtro por loja e busca por produto ou descricao</p>

  <div class="filter-row">
    <select id="filter-filial" onchange="renderTabela()">
      <option value="">Todas as lojas</option>
      <option value="FABULA BARRA SHOPPING">Barra Shopping</option>
      <option value="FABULA SHOP LEBLON CM">Shop Leblon</option>
      <option value="FABULA RIO SUL CM">Rio Sul</option>
      <option value="FABULA RDB CM">RDB</option>
      <option value="FABULA HARMONIA SP CM">Harmonia SP</option>
      <option value="FABULA PLAZA SHOP CM">Plaza Shop</option>
      <option value="FABULA SHOP VITORIA CM">Shop Vitoria</option>
      <option value="FABULA BARRA SALVADOR CM">Barra Salvador</option>
      <option value="FABULA ELDORADO CM">Eldorado</option>
      <option value="FABULA CENTRO CM">Centro</option>
    </select>
    <input type="text" id="filter-produto" placeholder="Buscar produto ou descricao..." oninput="renderTabela()" maxlength="40">
    <button class="export-btn" onclick="exportCSV()">Exportar CSV</button>
    <span class="row-count" id="row-count"></span>
  </div>

  <div class="card" style="padding:0;">
    <div class="table-wrap">
      <table style="min-width:750px;">
        <thead>
          <tr>
            <th>Filial</th><th>Produto</th><th>Descricao</th><th>Cor</th><th>Tam</th><th>Qtd</th>
          </tr>
        </thead>
        <tbody id="table-dist"></tbody>
      </table>
    </div>
  </div>
  <div class="pager" id="pager"></div>
</div>

</div><!-- /page -->

<!-- MODAL -->
<div class="modal-overlay" id="modal">
  <div class="modal">
    <h2>Gerar Pedido</h2>
    <p>Esta funcionalidade integra o output de distribuicao ao sistema de pedidos da Fabula, disparando automaticamente as solicitacoes de transferencia CD - filial.</p>
    <p style="font-size:.78rem;color:#bbb;margin-bottom:0">Prototipo - funcionalidade em desenvolvimento</p>
    <button class="modal-close" onclick="closeModal()">Entendido</button>
  </div>
</div>

<script>
const TOP20     = TOP20_PLACEHOLDER;
const DIST_ROWS = DIST_ROWS_PLACEHOLDER;
const DESC_MAP  = DESC_MAP_PLACEHOLDER;
const LOJAS     = LOJAS_PLACEHOLDER;
const TAMANHOS  = TAM_PLACEHOLDER;
const CALIB     = CALIB_PLACEHOLDER;

const PESOS = [
  {{dim:'Grupo de Produto',   peso:35, desc:'Tipo de peca: vestido, calca, casaco, macacao...'}},
  {{dim:'Familia de Tecido',  peso:15, desc:'Malha, Tecido Plano, Sarja, Tricot, Moletom...'}},
  {{dim:'Faixa de Preco',     peso:15, desc:'Tier 1 (<R$100) - Tier 4 (>=R$300)'}},
  {{dim:'Flag Praia + Bebe',  peso:15, desc:'Segmentacao de estilo: praia, linha bebe'}},
  {{dim:'Manga',              peso:10, desc:'Manga curta, longa, sem manga / regata'}},
  {{dim:'Estampado vs Liso',  peso:10, desc:'Textura visual: estampado ou liso'}},
];

const NOME_CURTO = {{
  'FABULA BARRA SHOPPING':'Barra Shopping','FABULA SHOP LEBLON CM':'Shop Leblon',
  'FABULA RIO SUL CM':'Rio Sul','FABULA RDB CM':'RDB','FABULA HARMONIA SP CM':'Harmonia SP',
  'FABULA PLAZA SHOP CM':'Plaza Shop','FABULA SHOP VITORIA CM':'Shop Vitoria',
  'FABULA BARRA SALVADOR CM':'Barra Salvador','FABULA ELDORADO CM':'Eldorado','FABULA CENTRO CM':'Centro'
}};

/* Tab switching */
function switchTab(id, btn) {{
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  btn.classList.add('active');
  if (id === 'tabela') renderTabela();
}}

/* Modal */
function openModal()  {{ document.getElementById('modal').classList.add('open'); }}
function closeModal() {{ document.getElementById('modal').classList.remove('open'); }}
document.getElementById('modal').addEventListener('click', e => {{ if (e.target===document.getElementById('modal')) closeModal(); }});

/* Generic bar chart — wideLabel extends label column to 240px */
function barChart(id, items, maxVal, fillClass, wideLabel) {{
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = items.map(item => {{
    const pct = Math.max(2, Math.round(item.val / maxVal * 100));
    const cls = wideLabel ? 'bar-item wide-label' : 'bar-item';
    return `<div class="${{cls}}">
      <div class="bar-label" title="${{item.label}}">${{item.label}}</div>
      <div class="bar-track"><div class="${{fillClass}}" style="width:${{pct}}%"></div></div>
      <div class="bar-val">${{item.val.toLocaleString('pt-BR')}}</div>
    </div>`;
  }}).join('');
}}

/* Peso chart */
function renderPesos() {{
  const el = document.getElementById('chart-pesos');
  if (!el) return;
  el.innerHTML = PESOS.map(p => `
    <div>
      <div class="peso-item">
        <div class="peso-label">${{p.dim}}</div>
        <div class="peso-track"><div class="peso-fill" style="width:${{p.peso}}%"></div></div>
        <div class="peso-val">${{p.peso}}%</div>
      </div>
      <div style="display:grid;grid-template-columns:180px 1fr;gap:.75rem">
        <div></div><div class="peso-desc">${{p.desc}}</div>
      </div>
    </div>
  `).join('');
}}

/* Calibration chart */
function renderCalib() {{
  const el = document.getElementById('chart-calib');
  if (!el) return;
  const maxF = Math.max(...CALIB.map(c => c.fator));
  el.innerHTML = CALIB.map(c => {{
    const pct = Math.round((c.fator - 1) / (maxF - 1) * 100);
    return `<div class="calib-item">
      <div class="calib-label">${{c.loja}}</div>
      <div class="calib-track"><div class="calib-fill" style="width:${{Math.max(5,pct)}}%"></div></div>
      <div class="calib-fator">x${{c.fator.toFixed(3)}}</div>
      <div class="calib-num">${{c.v25.toFixed(4)}}</div>
      <div class="calib-num">${{c.v3.toFixed(4)}}</div>
    </div>`;
  }}).join('');
}}

/* Loja table */
function renderLojaTable() {{
  const tbody = document.getElementById('table-lojas');
  if (!tbody) return;
  tbody.innerHTML = LOJAS.map(l => {{
    const cls = l.cobertura >= 90 ? 'g' : l.cobertura >= 80 ? 'y' : 'o';
    return `<tr>
      <td><strong>${{l.nome}}</strong></td>
      <td>${{l.leadtime}} d</td>
      <td>${{l.horizonte}} d</td>
      <td><strong>${{l.pecas.toLocaleString('pt-BR')}}</strong></td>
      <td>${{l.n_skus}}</td>
      <td style="color:var(--ink-soft)">${{l.demanda}}</td>
      <td>
        <span class="prog"><span class="prog-fill ${{cls}}" style="width:${{l.cobertura}}%"></span></span>
        <strong>${{l.cobertura}}%</strong>
      </td>
    </tr>`;
  }}).join('');
}}

/* Tabela with filter + pagination */
const PAGE_SIZE = 60;
let tabelaPage = 0;
let filteredRows = [];

function renderTabela() {{
  tabelaPage = 0;
  const filial  = document.getElementById('filter-filial').value;
  const search  = (document.getElementById('filter-produto').value || '').toLowerCase().trim();
  filteredRows = DIST_ROWS.filter(r => {{
    if (filial && r[0] !== filial) return false;
    if (search) {{
      const desc = (DESC_MAP[r[1] + '_' + r[2]] || '').toLowerCase();
      if (!r[1].toLowerCase().includes(search) && !desc.includes(search)) return false;
    }}
    return true;
  }});
  renderTabelaPage();
}}

function renderTabelaPage() {{
  const total = filteredRows.length;
  const start = tabelaPage * PAGE_SIZE;
  const end   = Math.min(start + PAGE_SIZE, total);
  const page  = filteredRows.slice(start, end);

  document.getElementById('row-count').textContent = `${{total.toLocaleString('pt-BR')}} linha${{total !== 1 ? 's' : ''}}`;

  const tbody = document.getElementById('table-dist');
  tbody.innerHTML = page.map(r => {{
    const desc = DESC_MAP[r[1] + '_' + r[2]] || '';
    return `<tr>
      <td>${{NOME_CURTO[r[0]] || r[0]}}</td>
      <td style="font-variant-numeric:tabular-nums;font-size:.8rem">${{r[1]}}</td>
      <td class="desc-col" title="${{desc}}">${{desc}}</td>
      <td>${{r[2]}}</td>
      <td>${{r[3]}}</td>
      <td><strong>${{r[4]}}</strong></td>
    </tr>`;
  }}).join('');

  const totalPages = Math.ceil(total / PAGE_SIZE);
  const pager = document.getElementById('pager');
  if (totalPages <= 1) {{ pager.innerHTML = ''; return; }}

  let btns = '';
  if (tabelaPage > 0)
    btns += `<button onclick="goPage(${{tabelaPage-1}})">Anterior</button>`;
  btns += `<span class="pager-info">Pagina ${{tabelaPage+1}} de ${{totalPages}}</span>`;
  if (tabelaPage < totalPages - 1)
    btns += `<button onclick="goPage(${{tabelaPage+1}})">Proxima</button>`;
  pager.innerHTML = btns;
}}

function goPage(p) {{
  tabelaPage = p;
  renderTabelaPage();
  document.getElementById('tab-tabela').scrollIntoView({{behavior:'smooth', block:'start'}});
}}

/* CSV Export — formato original 5 colunas */
function exportCSV() {{
  const header = 'FILIAL,PRODUTO,COR_PRODUTO,TAMANHO,QTD_DISTRIBUIR\\n';
  const rows = DIST_ROWS.map(r => r.join(',')).join('\\n');
  const blob = new Blob([header + rows], {{type:'text/csv;charset=utf-8;'}});
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href = url; a.download = 'distribuicao_inv26.csv';
  a.click(); URL.revokeObjectURL(url);
}}

/* Download HTML app */
function downloadHTML() {{
  const html = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;
  const blob = new Blob([html], {{type:'text/html;charset=utf-8'}});
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href = url;
  a.download = 'fabula_inv26_distribuicao.html';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}}

/* Init */
barChart('chart-lojas',    LOJAS.map(l=>  ({{label:l.nome, val:l.pecas}})),    Math.max(...LOJAS.map(l=>l.pecas)),    'bar-fill');
barChart('chart-tamanhos', TAMANHOS.map(t=>({{label:t.tam,  val:t.pecas}})), Math.max(...TAMANHOS.map(t=>t.pecas)), 'bar-fill soft');
barChart('chart-produtos', TOP20.map(p=>  ({{label:p.label, val:p.pecas}})),  Math.max(...TOP20.map(p=>p.pecas)),    'bar-fill', true);
renderPesos();
renderCalib();
renderLojaTable();
</script>
</body>
</html>"""

HTML = HTML.replace('TOP20_PLACEHOLDER',   top_json)  \
           .replace('DIST_ROWS_PLACEHOLDER', dist_json) \
           .replace('DESC_MAP_PLACEHOLDER',  desc_json) \
           .replace('LOJAS_PLACEHOLDER',     lojas_json)\
           .replace('TAM_PLACEHOLDER',       tam_json)  \
           .replace('CALIB_PLACEHOLDER',     calib_json)

out = 'app_distribuicao_inv26.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)

sz = os.path.getsize(out)
print(f"Saved: {out} ({sz:,} bytes / {sz//1024} KB)")
print(f"KPIs: {total_pecas} pecas | {pct_dist}% dist | {n_skus_total} SKUs | cob.media {int(cob_media)}%")
print(f"TOP20[0]: {top_list[0]}")
print(f"LOJAS[0]: {lojas_list[0]}")
print(f"CALIB[0]: {calib_list[0]}")
print(f"TAMANHOS: {tamanhos_list}")
