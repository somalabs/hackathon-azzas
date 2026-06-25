# Hackathon Azzas — Instruções do Projeto

> Este arquivo é carregado automaticamente pelo Claude Code quando alguém abre este
> repositório. Ele orienta como o Claude deve trabalhar com os times do hackathon.

## O que é

Hackathon de IA do grupo **Azzas 2154**, organizado pela **SomaLabs**. São **16 times**
distribuídos em **4 pilares estratégicos**. Cada time trabalha com o Claude e tem acesso
ao **MCP de dados Azzas** (BigQuery via agentes especializados).

## Os 4 pilares e os cases

| Pilar | Case |
|---|---|
| **Criativo** | Construir uma coleção cápsula de até 30 produtos: briefing/tema, produtos, ficha de repasse (simplificada) e produção de moda para showroom. |
| **Compras** | Construir a distribuição de peças da Fábula para a coleção do INV26. |
| **Eficiência Operacional** | Automatizar um fluxo operacional do dia a dia (ex.: portal de chamados, Feedz, PPT). |
| **Receita & Clientes** | Propor novas formas de segmentar a base de clientes da **Animale** (além de RFM/Matriz McKinsey) — agrupar para achar insights e oportunidades de negócio. |

Cada pilar tem uma **skill-guia** dedicada (`pilar-*`) que ativa automaticamente quando o
time conversa sobre o tema. Consulte `docs/` para onboarding e referências.

## Skills disponíveis neste repo

- **`azzas-dados`** — como usar o MCP de dados (escopo, roteamento, PII, tabelas). **Leia antes de qualquer análise de dados.**
- **`azzas-contexto-publico`** — contexto institucional público do grupo (marcas, estrutura, história).
- **`consulting-storytelling`** — estruturar apresentações no padrão de consultoria (todos os times apresentam no fim).
- **`pilar-criativo`**, **`pilar-compras`**, **`pilar-eficiencia-operacional`**, **`pilar-receita-clientes`** — guias por pilar.

## Regras de ouro (valem para todos os times)

1. **Nunca exponha dados pessoais (PII).** CPF, nome, e-mail, telefone, endereço, ID de
   cliente individual ou qualquer combinação que identifique uma pessoa **não podem**
   aparecer em nenhuma resposta, gráfico ou arquivo. Os agentes do MCP já recusam isso —
   **não tente contornar**. Sempre trabalhe com dados **agregados**.
2. **Nunca invente números.** Todo dado quantitativo vem de uma query do MCP nesta sessão
   ou foi fornecido pelo usuário. Se não tem o dado, diga que não tem — não estime sem rotular.
3. **Escopo antes de número de venda.** Para qualquer pergunta de venda/faturamento/receita,
   chame `azzas__escopo_de_venda` primeiro e confirme **canal + marca** com o time.
4. **Comparações são vs. LY** (mesmo período do ano anterior), salvo indicação contrária.
   Benchmarks externos de mercado não são usados.
5. **Sem dados confidenciais no repositório.** Este repo é **público**. Nunca commite
   números financeiros não-públicos, dados de clientes, ou material sensível. Trabalhe com
   esses dados apenas na sessão, nunca em arquivo versionado.

## Como o Claude deve atuar

- Seja um parceiro analítico direto: hipótese explícita, próximos passos claros, sem enrolação.
- Ao usar o MCP, siga o fluxo: `get_context` → `describe_table` → `get_business_rules` →
  `consultar_bq`. A skill `azzas-dados` detalha isso.
- Ajude o time a chegar num entregável apresentável (a skill `consulting-storytelling` ajuda no deck final).
