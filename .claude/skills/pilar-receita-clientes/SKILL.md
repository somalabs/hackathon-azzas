---
name: pilar-receita-clientes
description: >
  Guia do pilar RECEITA & CLIENTES do Hackathon Azzas. Use quando o time estiver trabalhando no
  case de segmentação: propor novas formas de segmentar a base de clientes, agrupar para achar
  insights e oportunidades de negócio. Acione em conversas sobre segmentação, clusterização,
  RFM, base de clientes, retenção/churn, CRM, LTV, personas, ou oportunidades de receita.
---

# Pilar Receita & Clientes — Segmentação da Base

## O case

> **Propor novas formas de segmentar a base de clientes.** Agrupe os clientes da melhor forma
> para encontrar insights e oportunidades de negócio.

A base do grupo tem +11 milhões de clientes. A forma como agrupamos define como falamos com eles,
o que oferecemos e onde está o crescimento. O case pede **uma segmentação nova e acionável** — não
só descritiva, mas que aponte oportunidades concretas.

## Entregável esperado

Uma **proposta de segmentação** com:
1. **A lógica de agrupamento** — quais variáveis, por quê, como os grupos se distinguem.
2. **Os segmentos** — perfil de cada um (tamanho, comportamento, valor) — sempre **agregado**.
3. **Os insights** — o que cada segmento revela que a visão atual não mostra.
4. **As oportunidades** — ações de negócio por segmento (aquisição, retenção, reativação, cross/upsell)
   e o tamanho potencial de cada uma.

## Dados disponíveis (via MCP — skill `azzas-dados`)

- **`clientes`** — a base central do case: segmentação Novo/Retido/Reativado, base ativa, RFM,
  árvore lógica por cliente (VA, ticket, frequência, PA). Duas perspectivas ("Ano de competência"
  vs "Janela móvel 12m") — declare qual está usando.
- **`midia_e_crm`** — já existe uma **clusterização McKinsey** (`clusterizacao_mckinsey`, 8 clusters,
  RFM) — ótimo ponto de partida e benchmark para a sua proposta. Também: retenção, churn, Share CRM,
  ROI por canal, performance de CRM por marca.
- **`vendas_linx`** — comportamento de compra (ticket, PA, categorias, markup) para enriquecer os segmentos.
- **`devolucoes`** — comportamento de devolução por perfil, sinal de (in)satisfação.

> ⚠️ **PII é linha vermelha aqui.** Você está mexendo com base de clientes. **Nunca** traga CPF,
> nome, e-mail, ID individual ou listas de clientes. `ClienteIdDia`/`ClienteID` = CPF — só dentro
> de agregação. Todo segmento é descrito por **estatística agregada**, nunca por indivíduos. Os
> agentes recusam o resto — não tente contornar.

## Abordagem sugerida

1. **Entenda a segmentação atual** — comece pela clusterização McKinsey existente para não reinventar a roda.
2. **Escolha um ângulo novo** — ex.: por estágio de ciclo de vida, por elasticidade a desconto,
   por multimarca vs monomarca, por canal de entrada, por sazonalidade, por categoria-âncora.
3. **Construa os grupos com dados** — agregue por dimensão; valide que os grupos são distintos e acionáveis.
4. **Encontre o "so what"** — para cada grupo, qual a oportunidade e seu tamanho (R$ ou nº de clientes).
5. **Priorize** — onde está o maior retorno com o menor esforço.

## Dicas

- Segmentação que não vira ação é só um relatório. Para cada segmento, responda **"e daí, o que fazemos?"**.
- Compare **vs LY** quando relevante (mesma régua do grupo).
- Use a skill `consulting-storytelling` para apresentar — segmentação fica ótima em matriz 2×2 e cards de persona.
