---
name: pilar-receita-clientes
description: >
  Guia do pilar RECEITA & CLIENTES do Hackathon Azzas. Use quando o time estiver trabalhando no
  case de segmentação: propor novas formas de segmentar a base de clientes da Animale, indo além
  de RFM e da Matriz McKinsey, para achar insights e oportunidades de negócio. Acione em conversas
  sobre segmentação, clusterização, RFM, Nobres & Liquideiros, base de clientes Animale,
  retenção/churn, CRM, LTV, personas, ciclo de vida da moda, ou oportunidades de receita.
---

# Pilar Receita & Clientes — Segmentação de Clientes Animale

## O case

> **Propor novas formas de segmentar a base de clientes da Animale.** Agrupe os clientes da
> melhor forma para encontrar insights e oportunidades de negócio — **indo além dos modelos
> existentes**.

O lema do playbook: **Analise + Inove + Impacte**. Não basta descrever a base; é preciso propor
uma **dimensão nova** de agrupamento e conectá-la a uma **alavanca de negócio real e mensurável**.

> 📄 Playbook oficial completo: [`docs/pilares/receita-clientes-animale.md`](../../../docs/pilares/receita-clientes-animale.md)
> (e o deck `receita-clientes-animale.pptx` na mesma pasta).

## Os modelos atuais (o ponto de partida — o desafio é superá-los)

Conheça os três para não reinventar a roda e para saber o que **já** é enxergado:

1. **RFM** — agrupa por **R**ecência (dias desde a última compra), **F**requência (nº de
   transações) e **M**onetário (valor acumulado). Segmentos: Champions, Loyal Customers, Potential
   Loyalist, Need Attention, At Risk, Can't Lose Them, Hibernating, Recent Customers.
2. **Matriz McKinsey: Valor × Frequência** — quadrantes:
   - Alta freq / Alto valor → fiéis de alto valor (balizas do que funciona).
   - Alta freq / Baixo valor → ama a marca, menor poder aquisitivo.
   - Baixa freq / Alto valor → compras pontuais de alto valor (olhar categoria/sazonalidade).
   - Baixa freq / Baixo valor → baixo envolvimento, experimentadoras.
   - Complementos: **Compra Única** (1 só compra — entender sazonalidade) e **Top Clientes** (DNA da marca).
3. **Nobres & Liquideiros** *(emergente)* — por **comportamento de preço**:
   - **Nobre**: desconto médio **≤ 20%** → paga preço justo, sinaliza valor de marca.
   - **Liquideiro**: desconto médio **> 20%** → sensível a preço, ativado por campanha/liquidação.

## Os ângulos que os modelos atuais NÃO enxergam (provocações)

Bons pontos de partida para a sua proposta (ou invente outro que os dados sugerirem):

- **Canal preferencial** — app, site desktop, loja física. O perfil de compra muda por canal?
- **Ciclo de vida da moda** — compra no lançamento ou no fim da curva? Básicos ou peças de destaque?
- **Estilo & categorias** — existe "cliente de vestido" vs "cliente de calça"? Os clusters se mantêm no tempo?
- **Risco de churn** — quais segmentos têm mais propensão a abandono? Quais têm mais potencial de upgrade/reativação?

## O que entregar (4 componentes)

| # | Componente | O que responder |
|---|---|---|
| **01** | **A Segmentação** | Lógica de agrupamento: quais variáveis, quantos segmentos, como cada um é caracterizado. |
| **02** | **O Tamanho da Base** | Quantas clientes em cada segmento e o peso financeiro (receita) de cada grupo. |
| **03** | **O Insight** | O que esse olhar revela que RFM/Matriz não enxergavam — a descoberta mais relevante. |
| **04** | **A Alavanca** | Qual ação de negócio o segmento habilita (campanha, produto, canal, oferta) — específica. |

Formato livre (slides, nota, planilha, oral). O que importa é a **clareza do raciocínio**.

## Dados disponíveis (via MCP — skill `azzas-dados`)

Foco em **Animale**. Agentes mais úteis:

- **`clientes`** — base central: segmentação Novo/Retido/Reativado, base ativa, RFM, árvore lógica
  (VA, ticket, frequência, PA). Duas perspectivas ("Ano de competência" vs "Janela móvel 12m") — declare qual usa.
- **`midia_e_crm`** — já tem a **clusterização McKinsey** (`clusterizacao_mckinsey`, 8 clusters) —
  ótimo benchmark. Também: retenção, churn, Share CRM, ROI por canal, comportamento por canal de CRM.
- **`vendas_linx`** — comportamento de compra Animale (ticket, PA, categorias, markup, **desconto** —
  insumo direto pro modelo Nobres & Liquideiros).
- **`devolucoes`** — devolução por perfil, sinal de (in)satisfação.

> ⚠️ **PII é linha vermelha.** Você mexe com base de clientes. **Nunca** traga CPF, nome, e-mail,
> ID individual ou listas. `ClienteIdDia`/`ClienteID` = CPF — só dentro de agregação. Todo segmento
> é descrito por **estatística agregada**. Os agentes recusam o resto — não tente contornar.

## Abordagem sugerida

1. **Calibre pelos modelos atuais** — rode RFM / Matriz / Nobres & Liquideiros na base Animale pra ter a régua.
2. **Escolha um ângulo novo** (canal, ciclo de moda, estilo, churn — ou outro).
3. **Construa os grupos com dados** — agregue, valide que são distintos e acionáveis, e dimensione (clientes + receita).
4. **Ache o "so what"** — o insight que os modelos atuais não davam.
5. **Conecte à alavanca** — a ação de negócio concreta e seu tamanho potencial.

## Dicas

- Segmentação que não vira ação é só relatório — para cada segmento responda **"e daí, o que fazemos?"**.
- Cruzar dimensões costuma render (ex.: Nobre × canal, ciclo de moda × churn).
- Compare **vs LY** quando relevante. Use `consulting-storytelling` pra apresentar (matriz 2×2 e cards de persona funcionam bem).
