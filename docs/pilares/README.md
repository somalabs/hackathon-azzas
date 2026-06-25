# Pilares e Cases

O hackathon trabalha 4 pilares estratégicos de IA na companhia. Cada pilar tem um case e uma
**skill-guia** dedicada que o Claude ativa automaticamente quando você conversa sobre o tema.

| Pilar | Case | Skill-guia |
|---|---|---|
| **Criativo** | Construir uma coleção cápsula de até 30 produtos: briefing/tema, produtos, ficha de repasse (simplificada) e produção de moda para showroom. | `pilar-criativo` |
| **Compras** | Construir a distribuição de peças da Fábula para a coleção do INV26. | `pilar-compras` |
| **Eficiência Operacional** | Automatizar um fluxo operacional do dia a dia (portal de chamados, Feedz, PPT...). | `pilar-eficiencia-operacional` |
| **Receita & Clientes** | Propor novas formas de segmentar a base de clientes para encontrar insights e oportunidades. | `pilar-receita-clientes` |

## Como usar

Não precisa abrir nada manualmente: ao conversar sobre o seu case, o Claude ativa a skill do
pilar e passa a seguir o guia (objetivo, dados disponíveis, abordagem, entregável, dicas).

Se quiser ler o conteúdo do guia diretamente, ele está em
`.claude/skills/pilar-<nome>/SKILL.md`.

## O que todo pilar tem em comum

- **Dados via MCP:** a skill `azzas-dados` orienta o Claude a usar os agentes de dados certos,
  com proteção de PII e o protocolo de escopo de venda. Veja a [referência do MCP](../recursos/mcp-dados.md).
- **Contexto do grupo:** a skill `azzas-contexto-publico` traz marcas, estrutura e história (dado público).
- **Apresentação final:** a skill `consulting-storytelling` ajuda a montar o deck no padrão de consultoria.

> Lembre-se das [regras do jogo](../onboarding/README.md#5-regras-do-jogo-importantes): PII nunca
> aparece, nada de inventar número, e nada confidencial no repositório.
