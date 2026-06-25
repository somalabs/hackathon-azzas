---
name: azzas-dados
description: >
  Use SEMPRE que o time precisar consultar dados do grupo Azzas via MCP de dados (BigQuery):
  vendas, faturamento, receita, ticket, markup, margem, base de clientes, segmentação,
  devoluções, atacado, mídia, CRM, ROAS, estoque, Farm Global, ou qualquer KPI de negócio.
  Ensina o protocolo de escopo de venda, o roteamento por agente, as regras de PII e o fluxo
  correto de consulta. Acione antes de chamar qualquer tool do gateway Azzas_MCP.
---

# Azzas — Guia do MCP de Dados

O grupo Azzas expõe seus dados por um **gateway MCP** (`Azzas_MCP`) com **8 agentes
especializados** sobre BigQuery. Cada agente cobre uma fatia do negócio e tem suas próprias
tabelas e regras. Esta skill ensina a usá-los com segurança e precisão.

## ⚠️ Antes de tudo: 3 regras inquebráveis

1. **PII nunca sai.** Nenhum dado que identifique uma pessoa (CPF, nome, e-mail, telefone,
   endereço, ID de cliente individual, ou combinação reidentificadora como filial+data+valor)
   pode aparecer em resposta, gráfico ou arquivo. Os agentes já recusam — **trabalhe sempre
   agregado** (GROUP BY por dimensão de negócio, faixas, contagens). `LIMIT` não resolve PII.
2. **Zero alucinação.** Todo número vem de uma query desta sessão ou do usuário. Sem dado →
   "não tenho esse dado". Use rótulos: ✅ real · 📈 LY · 🔶 estimativa · ❓ indisponível.
3. **Escopo antes de venda.** Para venda/faturamento/receita, chame `azzas__escopo_de_venda`
   **primeiro** e confirme canal + marca. Nunca assuma um canal por default.

## As tools de cada agente

Cada agente (`<agente>__<tool>`) expõe:

| Tool | Pra quê |
|---|---|
| `get_context` | Princípios, regras de PII e índice de tabelas do agente. **Chame 1x por agente antes de consultar.** |
| `describe_table` | Schema completo de uma tabela (colunas, tipos). |
| `get_business_rules` | SQL canônico, definições de KPI, casos especiais. **Leia antes de montar query não-trivial.** |
| `consultar_bq` | Executa a query (somente leitura). |
| `listar_analises` | Lista análises já publicadas. |
| `publicar_analise` | Publica snapshot HTML (v1). |
| `publicar_dashboard` | Publica dashboard interativo com filtros/cron (v2). |
| `ping` | Healthcheck. |

**Fluxo recomendado:** `escopo_de_venda` (se for venda) → `get_context` do agente →
`describe_table` das tabelas relevantes → `get_business_rules` → `consultar_bq`.

## Os 8 agentes — quando usar cada um

| Agente | Cobre | Use quando o time perguntar sobre… |
|---|---|---|
| `vendas_linx` | Vendas BR varejo + digital (8 marcas) | venda líquida, ticket, PA, markup, margem, CMV por marca/loja/produto |
| `clientes` | Base de clientes (ótica do cliente) | segmentação Novo/Retido/Reativado, base ativa, RFM, frequência, VA |
| `midia_e_crm` | Mídia paga + CRM + app | ROAS, Share CRM, e-mail/push/SMS/WhatsApp, clusters McKinsey, MAU/DAU |
| `devolucoes` | Trocas e devoluções BR (9 marcas) | volume/motivo de devolução, SLA de reversa |
| `ciclo_de_venda_atacado` | Atacado B2B marcas BR | sell-in, faturamento atacado, metas de representante, Somaplace, afiliados, **distribuição** |
| `farm_global` | Farm US/EU/UK varejo + digital | receita/ticket/markup Farm Global (multi-moeda) |
| `farm_global_atacado` | Wholesale internacional Farm | sell-in Joor, faturado wholesale, "verba" (MSRP) |
| `farm_global_devolucao` | Devoluções Farm Global (qualitativo) | motivos de devolução, CSAT/reviews Farm Global |

> Há um agente de people/RH no gateway, mas está **oculto** — não está disponível.

## Protocolo de escopo de venda (decorar)

Para a **1ª pergunta de venda da sessão sem escopo explícito**, chame
`azzas__escopo_de_venda` e pergunte ao time, em UMA mensagem, **em linguagem de negócio**:

1. **Canal** (pode marcar mais de um, ou "todos"): Varejo (lojas físicas) · Digital (e-commerce) · Atacado (B2B).
2. **Marca**: FARM · Animale · Fábula · NV · Maria Filó · Foxton · Cris Barros · Carol Bassi · Farm Global · (ou "todas"). Se FARM → perguntar "FARM, FARM ETC, ou ambos?".

**Nunca** ofereça nomes de sistema/agente como opção (isso é roteamento interno). Depois que
o time responder, traduza canal × marca em agente(s):

- Marca BR + Varejo/Digital → `vendas_linx__consultar_bq` (Varejo = `TIPO_VENDA='VENDA_LOJA'`; Digital = `VENDA_ECOM`/`VENDA_OMNI`/`VENDA_VITRINE`)
- Marca BR + Atacado → `ciclo_de_venda_atacado__consultar_bq`
- Farm Global + Varejo/Digital → `farm_global__consultar_bq` (Varejo = `st_channel` `STORE`/`CONCESSION`; Digital = `ONLINE`)
- Farm Global + Atacado → `farm_global_atacado__consultar_bq`

**Multi-agente:** consulte cada um e **consolide** — breakdown por canal (fonte explícita) +
total. Farm Global é multi-moeda (USD/EUR/GBP) → converta pra BRL antes de somar, com aviso de
câmbio. Máx. 2 agentes encadeados por turno. **Nunca** entregue a fatia de um agente como se
fosse o total. **Nunca zero silencioso:** combinação marca×canal sem dado (ex.: atacado de
Cris Barros / Carol Bassi) → avise que a operação existe mas o dado não está disponível aqui.

## Custo de query

Gate padrão: ≤10 GB executa direto; entre 10–15 GB confirme com o time; acima de 15 GB
reescreva a query. Filtre sempre por dimensão/coleção/data para não escanear a tabela inteira.

## Detalhes por agente

Para a lista completa de tabelas de cada agente, regras de negócio e colunas PII conhecidas,
veja **`references/agentes.md`**.
