# Pilares e Cases

O hackathon trabalha 4 pilares estratégicos de IA na companhia. Cada pilar tem um case e uma
**skill-guia** dedicada que o Claude ativa automaticamente quando você conversa sobre o tema.

| Pilar | Case | Skill-guia |
|---|---|---|
| **Criativo** | Criar uma coleção cápsula (até 30 produtos) a partir das próprias referências, gerando as imagens dos produtos no Freepik, e apresentá-la. | `pilar-criativo` |
| **Compras** | Construir um algoritmo de **distribuição inicial** da coleção INV26 da **Fábula** entre as 10 lojas físicas. | `pilar-compras` |
| **Eficiência Operacional** | Construir um agente de IA que lê uma base, gera uma visão e comunica os resultados automaticamente (Claude + Prompt + N8N). | `pilar-eficiencia-operacional` |
| **Receita & Clientes** | Propor novas formas de segmentar a base de clientes da **Animale**, além de RFM/Matriz McKinsey, para encontrar insights e oportunidades. | `pilar-receita-clientes` |

## Como usar

Não precisa abrir nada manualmente: ao conversar sobre o seu case, o Claude ativa a skill do
pilar e passa a seguir o guia (objetivo, dados disponíveis, abordagem, entregável, dicas).

Se quiser ler o conteúdo do guia diretamente, ele está em
`.claude/skills/pilar-<nome>/SKILL.md`.

## Playbooks oficiais por pilar

| Pilar | Material |
|---|---|
| Compras | [Briefing (Fábula INV26)](compras-fabula-inv26.md) · [`.docx`](compras-fabula-inv26.docx) · [deck `.pptx`](compras-fabula-inv26.pptx) |
| Eficiência Operacional | [Deck do participante](eficiencia-operacional.md) · [HTML interativo](eficiencia-operacional.html) |
| Receita & Clientes | [Playbook do participante (Animale)](receita-clientes-animale.md) · [deck `.pptx`](receita-clientes-animale.pptx) |
| Criativo | Workshop de geração de imagem (PDF na raiz do repo) + biblioteca de prompts em `.claude/skills/pilar-criativo/references/prompts-imagem.md` |

> 📦 **Arquivos de dados do case de Compras** (`compra`, `sortimento`, `leadtimes` da Fábula INV26)
> estão em [`compras-dados/`](compras-dados/) — são os insumos diretos do algoritmo.

## O que todo pilar tem em comum

- **Dados via MCP:** a skill `azzas-dados` orienta o Claude a usar os agentes de dados certos,
  com proteção de PII e o protocolo de escopo de venda. Veja a [referência do MCP](../recursos/mcp-dados.md).
- **Contexto do grupo:** a skill `azzas-contexto-publico` traz marcas, estrutura e história (dado público).
- **Apresentação final:** a skill `consulting-storytelling` ajuda a montar o deck no padrão de consultoria.
- **Padrão visual:** a skill `azzas-identidade-visual` aplica a identidade da Azzas (paleta, tipografia, componentes) em relatórios HTML, dashboards e slides.

> Lembre-se das [regras do jogo](../onboarding/README.md#5-regras-do-jogo-importantes): PII nunca
> aparece, nada de inventar número, e nada confidencial no repositório.
