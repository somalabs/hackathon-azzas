---
name: pilar-eficiencia-operacional
description: >
  Guia do pilar EFICIÊNCIA OPERACIONAL do Hackathon Azzas. Use quando o time estiver
  trabalhando no case de automação de processos: automatizar um fluxo operacional do dia a dia
  (portal de chamados, Feedz, geração de PPT, relatórios, etc.) com IA. Acione em conversas
  sobre automação, redução de custo/tempo, fluxo operacional, chamados, Feedz, RPA, integração
  de sistemas ou eliminação de trabalho manual.
---

# Pilar Eficiência Operacional — Automatizar um Fluxo

## O case

> **Automatizar um fluxo operacional do seu dia a dia.**
> Exemplos: portal de chamados, Feedz, geração de PPT, relatórios recorrentes.

A tese: automação de processos e redução de custo "ficou fácil de capturar" com IA. O objetivo é
pegar um processo **real, repetitivo e chato** do dia a dia e mostrar a IA fazendo o trabalho —
com ganho mensurável de tempo/qualidade.

## Entregável esperado

Um **fluxo automatizado funcionando** (ou um protótipo convincente), com:
1. **O processo "antes"** — passos manuais, tempo gasto, dores.
2. **A automação** — o que a IA/integração faz, ponta a ponta.
3. **O ganho** — tempo economizado, erros evitados, custo reduzido (estime e rotule).
4. **Como escalar** — o que falta para virar produção.

## Como o Claude ajuda

O Claude Code é ótimo para automação porque combina **raciocínio + execução de código + acesso
a ferramentas (MCP)**. Caminhos comuns:

- **Geração de documentos/PPT:** transformar dados ou texto bruto em relatório/apresentação
  estruturada (a skill `consulting-storytelling` ajuda na narrativa do deck).
- **Triagem e resposta:** classificar chamados/mensagens, sugerir resposta, rotear.
- **Extração e consolidação:** ler planilhas/PDFs/e-mails e consolidar em um formato único.
- **Integração via MCP:** vários sistemas do grupo já têm conectores MCP disponíveis na sessão
  (ex.: **Feedz**, dados Azzas, e outros). Use `ToolSearch` para descobrir as tools disponíveis
  e encadeá-las no fluxo.

## Abordagem sugerida

1. **Escolha um processo estreito e real** — melhor automatizar 100% de uma tarefa pequena do
   que 30% de uma grande. Procure algo repetitivo, baseado em regras e com volume.
2. **Mapeie o "antes"** — passos, inputs, outputs, tempo por execução, frequência.
3. **Desenhe o "depois"** — onde a IA decide, onde só executa, onde o humano valida.
4. **Construa o mínimo que funciona** — um caminho feliz ponta a ponta vale mais que slides.
5. **Meça** — tempo antes vs depois, % automatizado, erros evitados.

## Dicas

- **Ganho mensurável é o que ganha o case.** "Reduz de 2h para 5min, 40×/mês" convence.
- Cuidado com **dados sensíveis**: se o fluxo toca dados de pessoas, mantenha PII fora de
  qualquer saída e siga as regras do `CLAUDE.md`.
- Pense em **confiabilidade**: o que acontece quando a IA erra? Tenha o ponto de validação humana.
- Descubra ferramentas com `ToolSearch` — há conectores MCP além do de dados (ex.: Feedz para RH/engajamento).
