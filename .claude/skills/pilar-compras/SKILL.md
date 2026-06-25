---
name: pilar-compras
description: >
  Guia do pilar COMPRAS do Hackathon Azzas. Use quando o time estiver trabalhando no case de
  compras: construir a distribuição de peças da Fábula para a coleção do INV26. Acione em
  conversas sobre distribuição/alocação de produto, grade, sortimento, compra de coleção,
  sell-in vs sell-out, atacado, canais de venda da Fábula, ou planejamento de INV26.
---

# Pilar Compras — Distribuição da Fábula (INV26)

## O case

> **Construir a distribuição de peças da Fábula para a coleção do INV26.**

Compra e distribuição de produto são processos-chave do negócio: decidir **quanto de cada peça
vai para cada canal/ponto de venda** define giro, ruptura e markdown. A pergunta: como a IA pode
elevar a qualidade dessa decisão, usando dados de venda histórica, perfil de loja e comportamento
de coleção?

A **Fábula** é a marca infantil do grupo. INV26 = coleção **Inverno 2026** (`INV26`).

## Entregável esperado

Um **plano de distribuição** da coleção INV26 da Fábula: por peça (ou categoria) × canal/ponto
de venda, a quantidade/profundidade sugerida, com a **lógica e os dados** que sustentam a decisão
— e a leitura de risco (rupturas prováveis, excesso, peças-âncora).

## Dados disponíveis (via MCP — skill `azzas-dados`)

A Fábula vende em **varejo, digital e atacado**. Para distribuição, os agentes mais úteis:

- **`ciclo_de_venda_atacado`** — atacado/B2B da Fábula: sell-in por coleção, `programacao`
  (volume comprado por produto×coleção×canal, com sobra/falta/assertividade), metas, carteira
  de clientes B2B, devolução ao CD. **Filtre por `COLECAO`** (ex.: coleções de inverno anteriores
  como referência) e marca `FABULA`. Esta é a base central do case.
- **`vendas_linx`** — sell-out varejo + digital da Fábula: o que efetivamente vendeu por
  produto/loja/coleção, markup, desconto. Usar para entender demanda real por ponto de venda.
- **`devolucoes`** — devoluções da Fábula (`rede_lojas`), por motivo/produto — sinaliza erros
  de grade/qualidade que afetam distribuição.

> Atacado de algumas marcas pode não ter dado neste ambiente — confirme via `get_context`.
> A Fábula tem atacado disponível.

## Abordagem sugerida

1. **Entender a coleção e o histórico:** estrutura da INV26 (categorias, nº de peças) e como
   coleções de inverno anteriores performaram por canal/ponto de venda.
2. **Mapear demanda por ponto de venda:** cruzar sell-out (`vendas_linx`) com perfil de loja —
   que tipos de peça giram em cada cluster de loja/região.
3. **Avaliar assertividade passada:** `programacao` (atacado) mostra sobra/falta histórica —
   onde super/subdistribuímos antes.
4. **Propor a grade de distribuição:** profundidade por peça × canal/ponto, priorizando
   peças-âncora e respeitando capacidade.
5. **Quantificar o risco:** ruptura esperada, excesso, dependência de markdown.

## Dicas

- Sempre **agregue** (PII nunca aparece). Trabalhe por loja/cluster/região, não por cliente.
- Compare **vs LY** (mesma coleção do ano anterior) — é o comparativo padrão.
- Deixe a **lógica de alocação explícita** — o valor do entregável está no raciocínio, não só nos números.
- Use a skill `consulting-storytelling` para a apresentação final.
