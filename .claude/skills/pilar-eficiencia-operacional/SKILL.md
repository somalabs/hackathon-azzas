---
name: pilar-eficiencia-operacional
description: >
  Guia do pilar EFICIÊNCIA OPERACIONAL do Hackathon Azzas. Use quando o time estiver
  construindo um AGENTE DE ANÁLISE DE DADOS que automatiza um fluxo: ler uma base, gerar uma
  visão e comunicar os resultados sozinho. Acione em conversas sobre automação, agente de IA,
  N8N, fluxo automatizado, Prompt, integração (e-mail/Teams/painel), análise automática de
  dados, ou redução de trabalho manual.
---

# Pilar Eficiência Operacional — Construir um Agente de IA

## O case

> **Crie um agente de análise de dados.** A partir de uma base de dados, o agente deve **gerar
> uma visão e comunicar os resultados automaticamente** — ponta a ponta, sem trabalho manual.

O espírito do pilar: automação de processos + IA ficou fácil de capturar. Hoje você constrói o seu
**primeiro agente de verdade** e o vê trabalhar do início ao fim.

> 📄 Deck oficial do participante: [`docs/pilares/eficiencia-operacional.md`](../../../docs/pilares/eficiencia-operacional.md)
> (versão HTML interativa `eficiencia-operacional.html` na mesma pasta).

## Os 3 passos do agente

| # | Passo | O que faz |
|---|---|---|
| **01** | **Ler a base** | Acessa a base de dados e entende a estrutura das informações. |
| **02** | **Gerar a visão** | Analisa os dados e produz os principais números, recortes e insights. |
| **03** | **Comunicar** | Envia os resultados automaticamente — por e-mail, Teams ou um painel. |

## As peças (como tudo se conecta)

**Prompt + Claude + N8N = Agente.**

- **Prompt** — a *instrução* que você dá à IA. Quanto mais clara, melhor o resultado.
  Fórmula: **papel + tarefa + dados + formato**. (Ex. fraco: "analise as vendas". Ex. forte:
  "Você é um analista. Calcule vendas e MKP por marca, região e estado a partir deste CSV e liste
  3 destaques em 5 linhas.")
- **Claude** — o *cérebro*: lê e resume, escreve, analisa dados, gera código/páginas.
- **N8N** — os *braços* que conectam tudo: ferramenta visual de automação (blocos tipo Lego) que
  liga apps (e-mail, Teams, Drive, bancos de dados) sem programar do zero. Estrutura de um fluxo:
  **Gatilho** (horário/arquivo/clique) → **Conectores** (apps) → **Nó de IA** (Claude) → **Saídas** (enviar/publicar/salvar/avisar).

> Automação tradicional **segue regras fixas** e trava no inesperado. Automação **com IA**
> interpreta, decide e lida com o que foge do padrão. A automação *faz*, a IA *entende* — juntas
> resolvem o que antes exigia uma pessoa.

## Formato

Em equipes · **2h15 de execução** · **3 entregáveis** · apresentação final.

## Dados disponíveis (via MCP — skill `azzas-dados`)

A "base de dados" do agente pode ser o MCP de dados Azzas (vendas, clientes, devoluções, mídia/CRM,
atacado, Farm Global) — o Claude lê e analisa com o protocolo de escopo e as regras de PII. Você
também pode usar uma base própria (CSV/planilha) que o time trouxer.

> ⚠️ Se o agente toca dados de pessoas, mantenha **PII fora** de qualquer saída (e-mail, painel,
> mensagem). Trabalhe sempre agregado — ver `CLAUDE.md` e a skill `azzas-dados`.

## Abordagem sugerida

1. **Escolha o fluxo** — uma análise recorrente e chata que valha a pena automatizar (ex.: um
   resumo diário/semanal de um indicador, enviado pro time).
2. **Defina o Prompt** — papel + tarefa + dados + formato; teste e refine no Claude.
3. **Monte o agente** — ligue base → Claude (análise) → canal de comunicação. Use N8N para
   orquestrar gatilho e envio, ou monte o fluxo direto no Claude se for suficiente.
4. **Rode ponta a ponta** — um caminho feliz completo vale mais que slides.
5. **Mostre o ganho** — tempo antes vs depois, frequência, erros evitados.

## Dicas

- **Estreito e completo** > amplo e pela metade: automatize 100% de uma tarefa pequena.
- **Ganho mensurável ganha o case** — "de 2h para 5min, 40×/mês" convence.
- Pense na **confiabilidade**: o que acontece quando a IA erra? Tenha ponto de validação humana.
- Para a comunicação final, capriche no formato (a skill `azzas-identidade-visual` padroniza
  painéis/relatórios; `consulting-storytelling` ajuda na apresentação).
