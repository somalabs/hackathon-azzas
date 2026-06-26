---
name: pilar-compras
description: >
  Guia do pilar COMPRAS do Hackathon Azzas. Use quando o time estiver trabalhando no case:
  construir um algoritmo/solução de DISTRIBUIÇÃO INICIAL da coleção Inverno 2026 (INV26) da
  Fábula entre as 10 lojas físicas. Acione em conversas sobre distribuição inicial, alocação de
  estoque, grade de tamanhos, sortimento, leadtime, estoque regulador, ressuprimento, cobertura
  de venda, priorização de filiais, ou o desafio Fábula INV26.
---

# Pilar Compras — Distribuição Inicial da Fábula (INV26)

## O case

> Criar um **algoritmo / solução / plataforma** que automatize e otimize a **distribuição
> inicial** da coleção **Inverno 2026 (INV26)** da Fábula entre as **10 lojas físicas** — a
> carga de estoque que cada loja recebe no lançamento, antes do ressuprimento automático assumir.

**Por que importa:** o ressuprimento automático precisa de **14 dias** de venda em loja para
calibrar. Nesse período de aquecimento, cada loja depende **só** do que recebeu na distribuição
inicial. Distribuir **pouco** → ruptura antes do ressuprimento assumir. Distribuir **demais** →
esvazia o CD e compromete o estoque regulador que abastece as lojas depois. O desafio é o equilíbrio.

> 📄 Briefing completo: [`docs/pilares/compras-fabula-inv26.md`](../../../docs/pilares/compras-fabula-inv26.md)
> · deck `compras-fabula-inv26.pptx` na mesma pasta · arquivos de dados: ver onboarding do pilar.

## Números do desafio

- **10 filiais físicas** (e-commerce **fora do escopo** — ignore `FABULA ECOMMERCE CM` e `FABULA ECOMMERCE SP CM`).
- **298 produto-cor**, **57.112 peças** compradas. Tamanhos por **posição de grade** (`TAM_1`…`TAM_6`), não PP/P/M/G.
- **Horizonte de cobertura por filial = 14 + leadtime** dias (ex.: Salvador leadtime 16 → 30 dias; Leblon leadtime 4 → 18 dias).
- ⚠️ **Data-base: 31/03/2026.** Nenhum dado de venda/estoque posterior pode entrar no algoritmo (vazamento de informação / quebra de reprodutibilidade). INV26 é coleção passada justamente pra permitir comparar resultados.

## Arquivos de entrada (insumos diretos)

| Arquivo | Define | Colunas-chave |
|---|---|---|
| `compra_INV26_lancamento_fabula.xlsx` | Volume comprado (= total disponível p/ distribuir) | `PRODUTO`, `COR_PRODUTO`, `DESCRICAO`, `COMPRA`, `TAM_1`…`TAM_6` |
| `sortimento_INV26_lancamento_fabula.xlsx` | Quais produto-cor **podem** ir p/ cada filial | `FILIAL`, `PRODUTO`, `COR_PRODUTO`, `SORTIMENTO` (SIM/NÃO) |
| `leadtimes_INV26_lancamento_fabula.xlsx` | Dias de trânsito CD → filial | `FILIAL`, `LEADTIME` |

`SORTIMENTO=NÃO` = proibido enviar; `SIM` = pode (não obriga). 49 de 2.980 combinações são "NÃO".

## Dados adicionais (via MCP — skill `azzas-dados`)

Histórico de vendas, estoque e cadastro de produto p/ **estimar demanda, calibrar velocidade de
venda e priorizar filiais**. Use o agente **`vendas_linx`** (sell-out Fábula varejo por produto/
loja/coleção — coleções de inverno anteriores como proxy), e `ciclo_de_venda_atacado` / `devolucoes`
se útil. **Sem dado posterior a 31/03/2026.** Sempre agregado (PII nunca aparece).

## Regras de negócio obrigatórias (hard constraints)

1. **Sortimento:** `SORTIMENTO=NÃO` → zero unidades p/ aquela filial-produto-cor, em qualquer tamanho.
2. **Estoque comprado:** soma distribuída de um produto-cor-tamanho entre filiais ≤ `TAM_N` comprado. Só inteiros não-negativos.
3. **Mínimo por SKU:** se enviar, ao menos 1 unidade. Zero não aparece no output — omite a linha.
4. **Completude de grade:** se o estoque restante cobre só uma fração pequena dos tamanhos, pode ser melhor não enviar nada. **O time define e documenta o limiar.**
5. **Exclusão de e-commerce:** nenhuma unidade p/ os canais de e-commerce.

> Exceção permitida: o time **pode** propor uma **nova clusterização/sortimento** das lojas — desde que com racional baseado em dados.

## Decisões em aberto (o time decide e justifica)

- **Estimativa de demanda:** que proxy histórico usar (similares, categoria, sazonalidade)? Em que granularidade? Como tratar produtos sem análogo?
- **Priorização de filiais:** por volume/faturamento histórico? perfil de produto por loja? geografia? combinação ponderada? (A Fábula **não** tem clusterização oficial de lojas.)
- **Priorização dentro da grade:** quando falta um tamanho, qual filial leva?
- **Limiar de completude de grade:** % mínimo de tamanhos, nº mínimo, ou outro critério.

## Output esperado

Tabela de distribuição: **`FILIAL` · `PRODUTO` · `COR_PRODUTO` · `TAMANHO` (1–6) · `QTD_DISTRIBUIR` (≥1)**.
Linhas com 0 não aparecem. **Validar antes de entregar:** sem violação de sortimento, soma ≤ estoque
comprado por produto-cor-tamanho, sem e-commerce, todos inteiros ≥ 1.

## Entregáveis

1. **Código/plataforma** que recebe os inputs e gera o output (roda sem intervenção manual, reprodutível).
2. **Arquivo de output** com a distribuição.
3. **Documentação das decisões** (demanda, priorização, limiar de grade) com justificativa baseada em dados.
4. **Análise de cobertura:** por filial, % de produto-cor que atinge (14+leadtime) dias, cobertura mediana, % de SKUs em risco de ruptura.

## Critérios de avaliação

| Critério | Peso |
|---|---|
| Cobertura de demanda (% filial-produto que atinge o alvo sem ruptura) | Alto |
| Eficiência do estoque (% distribuído vs. retido no regulador sem necessidade) | Alto |
| **Respeito às restrições duras** (zero violações) | **Eliminatório** |
| Reprodutibilidade (roda sem intervenção, mesmo resultado, sem usar dados INV26 pós-data-base) | Alto |
| Qualidade da decisão sobre grade | Médio |
| Fundamentação das decisões | Médio |

## Dicas

- Comece validando os **hard constraints** — uma violação é eliminatória.
- O alvo de cobertura é **(14 + leadtime)** — leadtime alto (Salvador, Vitória) exige mais profundidade.
- Otimizar distribuição = otimizar o **estoque regulador**: cada peça a mais numa loja é uma a menos no CD.
- Deixe as decisões da seção "em aberto" **explícitas e justificadas com dados** — vale nota.
- Use `consulting-storytelling` p/ a apresentação final.
