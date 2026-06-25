# Referência — MCP de Dados Azzas

O grupo expõe seus dados por um **gateway MCP** (`Azzas_MCP`) com **8 agentes especializados**
sobre BigQuery (somente leitura). Esta é a referência humana; o Claude usa a skill `azzas-dados`
(em `.claude/skills/azzas-dados/`) para operar o MCP no caminho certo.

## Regras inquebráveis

1. **PII nunca sai.** CPF, nome, e-mail, telefone, endereço, ID de cliente individual ou
   combinações reidentificadoras não aparecem — só dados **agregados**. Os agentes recusam o resto.
2. **Zero alucinação.** Todo número vem de uma query da sessão ou do usuário. Sem dado → "não tenho".
3. **Escopo antes de venda.** Para venda/receita, o Claude chama `azzas__escopo_de_venda` e
   confirma **canal + marca** antes de puxar número.

## Os 8 agentes

| Agente | Cobre |
|---|---|
| `vendas_linx` | Vendas BR varejo + digital (8 marcas): receita, ticket, PA, markup, margem, CMV |
| `clientes` | Base de clientes: segmentação Novo/Retido/Reativado, base ativa, RFM, frequência |
| `midia_e_crm` | Mídia paga, CRM (e-mail/push/SMS/WhatsApp), ROAS, Share CRM, clusters McKinsey, app MAU/DAU |
| `devolucoes` | Trocas e devoluções BR (9 marcas): volume, motivo, SLA de reversa |
| `ciclo_de_venda_atacado` | Atacado B2B marcas BR: sell-in, faturamento, metas, Somaplace, afiliados, distribuição |
| `farm_global` | Farm US/EU/UK varejo + digital (multi-moeda) |
| `farm_global_atacado` | Wholesale internacional Farm (Joor, faturado, "verba"/MSRP) |
| `farm_global_devolucao` | Devoluções Farm Global (qualitativo: motivos, CSAT) |

> Há um agente de people/RH no gateway, mas está **oculto** — indisponível.

## Tools de cada agente

`get_context` (índice de tabelas + regras) · `describe_table` (schema) · `get_business_rules`
(SQL canônico/KPIs) · `consultar_bq` (executa query) · `listar_analises` · `publicar_analise`
(HTML) · `publicar_dashboard` (interativo) · `ping`.

Tool de roteamento: **`azzas__escopo_de_venda`** — chamada primeiro em qualquer pergunta de venda.

**Fluxo:** escopo (se venda) → `get_context` → `describe_table` → `get_business_rules` → `consultar_bq`.

## Roteamento de venda (canal × marca)

| Marca | Canal | Agente |
|---|---|---|
| Marca BR (FARM, Animale, Fábula, NV, Maria Filó, Foxton, Cris Barros, Carol Bassi) | Varejo / Digital | `vendas_linx` |
| Marca BR | Atacado | `ciclo_de_venda_atacado` |
| Farm Global | Varejo / Digital | `farm_global` |
| Farm Global | Atacado | `farm_global_atacado` |

Multi-agente → consolidar (Farm Global é multi-moeda → converter pra BRL antes de somar). Máx. 2
agentes por turno. Nunca entregar a fatia de um agente como se fosse o total. Atacado de Cris
Barros / Carol Bassi: operação existe, mas sem dado neste ambiente.

## Custo de query

≤10 GB executa direto · 10–15 GB pede confirmação · >15 GB reescrever. Sempre filtrar por
dimensão/coleção/data.

## Detalhe completo (tabelas por agente)

Veja `.claude/skills/azzas-dados/references/agentes.md` — lista de tabelas, regras de negócio e
colunas PII conhecidas de cada agente.
