# Handoff — Pilar Compras · Fábula INV26

> Leia este arquivo no início de uma nova conversa com o Claude para retomar exatamente de onde paramos.
> Instrução: "Leia HANDOFF_COMPRAS.md e continue o trabalho de onde paramos."

---

## Contexto do case

**Objetivo:** construir um algoritmo de distribuição inicial da coleção INV26 da Fábula entre 10 lojas físicas.

**Regras eliminatórias:**
- `SORTIMENTO = NÃO` → zero unidades para aquela filial-produto-cor
- Soma distribuída ≤ estoque comprado por produto-cor-tamanho
- Somente inteiros ≥ 1 (ou 0, sem aparecer no output)
- Excluir e-commerce do escopo

**Output esperado:** tabela com colunas `FILIAL · PRODUTO · COR_PRODUTO · TAMANHO · QTD_DISTRIBUIR`

---

## Escopo MCP confirmado

- **Marca:** Fábula → `RL_DESTINO = 5` / `CAST(RL_DESTINO AS STRING) = '5'`
- **Canal:** Varejo físico → `TIPO_VENDA = 'VENDA_LOJA'`
- **Agente MCP:** `vendas_linx`
- **Proxy histórico:** INV23, INV24, INV25 (coleções de inverno anteriores)

---

## Arquivos de entrada (xlsx — não modificar)

| Arquivo | Conteúdo |
|---|---|
| `docs/pilares/compras-dados/compra_INV26_lancamento_fabula.xlsx` | 298 produto-cor, 57.112 peças. Colunas: PRODUTO, COR_PRODUTO, DESCRICAO, COMPRA, TAM_1…TAM_6 |
| `docs/pilares/compras-dados/sortimento_INV26_lancamento_fabula.xlsx` | 2.980 linhas. Colunas: FILIAL, PRODUTO, COR_PRODUTO, SORTIMENTO (SIM/NÃO). 49 NÃO. |
| `docs/pilares/compras-dados/leadtimes_INV26_lancamento_fabula.xlsx` | 10 filiais com LEADTIME (dias). Horizonte = 14 + leadtime. |

---

## Arquivos gerados

| Arquivo | Descrição |
|---|---|
| `produtos_inv26_attrs.csv` | Atributos INV26 do catálogo BQ. 252 produtos encontrados de 298. |
| `historico_inv_vendas.csv` | Vendas históricas INV23/24/25 × 10 filiais. 9.063 linhas. |
| `historico_attrs_precos.csv` | Atributos + preços históricos INV23/24/25. 2.839 produtos. |
| `velocidade_prevista_inv26_v2.csv` | Deprecado. v2 com ON_DAYS=122 para todas as coleções. |
| `velocidade_prevista_inv26_v3.csv` | Deprecado. v3 com ON_DAYS corrigidos mas sem calibração. |
| `velocidade_prevista_inv26_v4.csv` | **[USAR ESTE]** 2.990 linhas. Colunas extras: `calib_fator`, `velocidade_calibrada`. Demanda total: 3.541 pcs. |
| `similarity_analysis_v2.py` | Modelo v2 (referência histórica). |
| `similarity_analysis_v3.py` | Modelo v3 com ON_DAYS corrigidos. |
| `similarity_analysis_v4.py` | **[ATUAL]** Modelo v4 = v3 + calibração por loja. Reprodutível. |
| `distribuicao_inv26.py` | **[ATUAL]** Algoritmo de distribuição. Usa v4. GRADE_THRESH=0.25. |
| `distribuicao_inv26.csv` | **[OUTPUT FINAL]** 3.076 linhas. 3.115 pcs distribuídas. 4 validações OK. |
| `app_distribuicao_inv26.html` | **[APP]** SPA estático 168 KB. 4 tabs: Visão Geral, Por Loja, Por Produto, Validações. Botão "Gerar Pedido" + export CSV. Abrir no browser. |
| `produtos_inv26.txt` | Lista de códigos de produto INV26 para queries BQ. |

---

## O que foi feito — resumo

### 1. Exploração dos dados de entrada
- 298 produto-cor, 57.112 peças, 10 filiais físicas, 49 restrições de sortimento
- Filiais críticas por leadtime: **Salvador (16 d → horizonte 30 d)** e **Vitória (11 d → horizonte 25 d)**
- Grades: maioria 4 tamanhos (TAM_1–4); 52 produtos com 5 tamanhos

### 2. Análise de similaridade — evolução dos modelos

| Versão | Novidade | Demanda total |
|---|---|---|
| v1 | 3 dimensões | — |
| v2 | 6 dimensões + pesos | 3.360 pcs |
| v3 | ON_DAYS correto por coleção (INV23=122d, INV24=214d, INV25=206d) + crescimento +11,1% | 2.845 pcs |
| **v4** | **Calibração por loja âncora ao INV25 real × crescimento** | **3.541 pcs** |

**Por que v3 estava abaixo do INV25:** correção do ON_DAYS reduz velocidade em 1,69×; growth de 11,1% compensa parcialmente (redução líquida ~34%). Lojas com pouco dado INV25 (Leblon, Harmonia) sofriam mais pois o KNN caía no INV24 (ON_DAYS=214). Fatores de calibração v4: ×1,26 (Barra Shopping) a ×1,68 (Leblon CM).

### 3. Análise de similaridade (modelo v4)

**Lógica:** como INV26 não tem histórico de venda, mapeamos cada produto INV26 para os 15 produtos mais similares das coleções INV23/24/25. Usamos a velocidade de venda desses similares como previsão.

**6 dimensões com pesos:**
| Dimensão | Fonte | Peso |
|---|---|---|
| GRUPO_PRODUTO (tipo de peça) | PRODUTOS BQ | 0,35 |
| Faixa de preço (tier 1–4) | PRODUTOS_PRECOS VO/V | 0,15 |
| Família de tecido | parse de LINHA | 0,15 |
| Estilo de manga | parse de SUBGRUPO_PRODUTO | 0,10 |
| Estampado vs Liso | parse de LINHA | 0,10 |
| Flag Praia + Flag Bebê | LINHA + DESC_PRODUTO | 0,15 |

**Faixas de preço:**
- Tier 1: < R$100
- Tier 2: R$100–199
- Tier 3: R$200–299
- Tier 4: ≥ R$300

**Pesos de coleção (para calcular velocidade ponderada):**
- INV23: peso 1,0
- INV24: peso 2,0
- INV25: peso 3,0

**Janela ON-season:** 122 dias por coleção (Jun–Set de cada ano)

### 3. Resultado de velocidade por filial (v4 — calibrado)

| Filial | Vel. calibrada (pcs/dia) | Horizonte | Demanda prevista | Peças distribuídas | Cobertura |
|---|---|---|---|---|---|
| Barra Salvador CM | 0,057 | **30 dias** | 581 | 559 | 96,2% |
| Shop Vitória CM   | 0,058 | **25 dias** | 434 | 401 | 92,4% |
| Barra Shopping    | 0,078 | 18 dias | 401 | 362 | 90,3% |
| Shop Leblon CM    | 0,070 | 18 dias | 386 | 350 | 90,7% |
| Rio Sul CM        | 0,061 | 18 dias | 337 | 290 | 86,1% |
| Harmonia SP CM    | 0,046 | 20 dias | 320 | 273 | 85,3% |
| RDB CM            | 0,056 | 18 dias | 303 | 253 | 83,5% |
| Eldorado CM       | 0,047 | 20 dias | 282 | 235 | 83,3% |
| Plaza Shop CM     | 0,043 | 18 dias | 285 | 226 | 79,3% |
| Centro CM         | 0,026 | 18 dias | 212 | 166 | 78,3% |

**Demanda prevista v4: 3.541 pcs · Distribuídas: 3.115 pcs · CD regulador: 53.997 pcs (94,5%)**

### 4. Algoritmo de distribuição — decisões tomadas

- **Prioridade de escassez:** leadtime decrescente (Salvador e Vitória primeiro)
- **Completude de grade:** ≥ 25% dos tamanhos ativos devem ter ≥ 1 unidade
- **Arredondamento:** maior resto (sem viés, soma exata)
- **Threshold de envio:** demanda ≥ 0,3 → envia pelo menos 1 unidade

### 5. Resultado da distribuição (distribuicao_inv26.csv)

- **3.076 linhas** no output final
- **3.115 peças** distribuídas (5,5% do estoque)
- Todas as 4 validações ✅: sortimento, estoque, mínimo=1, sem ecommerce
- Centro CM: 166 pcs (antes estava zerado com GRADE_THRESH=50%)

---

## STATUS: CONCLUÍDO

Todos os entregáveis estão prontos. Para retomar, abra `app_distribuicao_inv26.html` no browser.

---

## Informações técnicas úteis

### Schema BQ relevante (agente vendas_linx)
- Tabela principal: `soma-pipeline-prd.silver_linx.TB_WANMTP_VENDAS_LOJA_CAPTADO`
- Produto master: `soma-pipeline-prd.silver_linx.PRODUTOS`
- Preços: `soma-pipeline-prd.silver_linx.PRODUTOS_PRECOS` (códigos: CT=custo, VO=original, V=varejo)
- Filiais: `soma-pipeline-prd.silver_linx.FILIAIS` (join: CODIGO_FILIAL_DESTINO = COD_FILIAL)
- Fábula = `RL_DESTINO = 5` (INTEGER → cast para STRING no join)

### Mapeamento de filiais (nome no sortimento → nome histórico BQ)
```python
STORE_MAP = {
    "FABULA SHOP LEBLON CM":    ["FABULA SHOP LEBLON CM"],
    "FABULA BARRA SHOPPING":    ["FABULA BARRA SHOPPING"],
    "FABULA RIO SUL CM":        ["FABULA RIO SUL CM"],
    "FABULA RDB CM":            ["FABULA RDB CM"],
    "FABULA HARMONIA SP CM":    ["FABULA HARMONIA SP CM"],
    "FABULA PLAZA SHOP CM":     ["FABULA PLAZA SHOP CM"],
    "FABULA SHOP VITORIA CM":   ["FABULA SHOP VITORIA CM"],
    "FABULA BARRA SALVADOR CM": ["FABULA BARRA SALVADOR CM"],
    "FABULA ELDORADO CM":       ["FABULA ELDORADO CM"],
    "FABULA CENTRO CM":         ["FABULA CENTRO CM"],
}
```

---

## Como usar este arquivo na próxima conversa

Abra uma nova sessão do Claude Code neste repositório e envie:

> "Leia o arquivo HANDOFF_COMPRAS.md e continue de onde paramos. O próximo passo é construir o algoritmo de distribuição usando o arquivo velocidade_prevista_inv26_v2.csv como base de demanda."
