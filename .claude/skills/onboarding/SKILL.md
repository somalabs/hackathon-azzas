---
name: onboarding
description: >
  Fluxo de boas-vindas do Hackathon Azzas. Use no INÍCIO da sessão de um participante — ou quando
  alguém disser "oi", "vamos começar", "sou novo", "por onde começo", "me situa", "onboarding" —
  para dar as boas-vindas, entrevistar a pessoa/time (background, contexto, pilar/desafio,
  ferramentas, expectativa) e direcionar pro material e próximos passos certos.
---

# Onboarding do Participante — Hackathon Azzas

Seu papel aqui é receber o time, entender com quem você está falando e em que vão trabalhar, e
deixá-los prontos pra começar. Conduza como uma conversa rápida e calorosa — **não despeje todas as
perguntas de uma vez**. Faça em rodadas curtas, reaja ao que responderem e calibre o resto da
sessão pelo que aprender (nível técnico, pilar, objetivo).

> Quando fizer perguntas de múltipla escolha (ex.: o pilar), use um formato de opções claro.
> Pule qualquer pergunta que a pessoa já tiver respondido espontaneamente.

## Abertura (1 parágrafo)

Dê as boas-vindas ao Hackathon Azzas e explique em uma frase o que vai acontecer: "São 4 pilares
de IA; seu time pega um e entrega uma solução usando o Claude + os dados da Azzas; no fim, todos
apresentam." Diga que vai fazer algumas perguntas rápidas pra te situar e já te apontar o caminho.

## Rodada 1 — Quem é o time

- **Quem são vocês?** Nome do time / integrantes e suas áreas ou funções (ex.: estilo, planejamento, dados, comercial, marketing).
- **Familiaridade com IA / Claude / dados** — de "nunca usei" a "mexo todo dia". Isso calibra quanto detalhe técnico usar no resto da sessão.

## Rodada 2 — O desafio (pilar)

Pergunte **qual pilar** vão atacar, com as 4 opções:

1. **Criativo** — criar uma coleção cápsula (até 30 produtos) a partir das próprias referências, gerando imagens no Freepik.
2. **Compras** — algoritmo de distribuição inicial da coleção INV26 da Fábula entre as 10 lojas.
3. **Eficiência Operacional** — construir um agente de IA que lê uma base, gera uma visão e comunica sozinho.
4. **Receita & Clientes** — nova forma de segmentar a base de clientes da Animale.

Ao saber o pilar, **acione a skill do pilar** correspondente (`pilar-criativo`, `pilar-compras`,
`pilar-eficiencia-operacional`, `pilar-receita-clientes`) e siga com 1–2 perguntas específicas:

- **Criativo:** que estética/marca/público inspira vocês? Já têm referências em mente? Já usaram Freepik ou IA de imagem?
- **Compras:** o time está confortável com dados/lógica de algoritmo? Que linguagem/ferramenta pretendem usar? (Os dados de entrada estão em `docs/pilares/compras-dados/`.)
- **Eficiência:** que processo chato do dia a dia querem automatizar? Pretendem usar N8N? Qual será a base de dados (MCP Azzas ou própria)?
- **Receita & Clientes:** algum ângulo de segmentação que já curtem (canal, ciclo de moda, churn, preço)? Confortáveis com análise de dados via MCP?

## Rodada 3 — Recursos e expectativa

- **Ferramentas:** sabem que o **MCP de dados já vem conectado** no Claude? Vão usar também Freepik (criativo) / N8N (eficiência) / IAZZAS (interface web)?
- **Objetivo:** o que vocês imaginam entregar? Já têm uma ideia ou querem ajuda pra definir o escopo?

## Fechamento — Direcione

Com base nas respostas:
1. Reforce as **regras de ouro** rapidamente: dados pessoais (PII) nunca aparecem; nada de inventar número; o repo é público (sem dado confidencial commitado).
2. Aponte o **material do pilar** (em `docs/pilares/`) e diga que a skill do pilar já está ativa.
3. Proponha um **primeiro passo concreto** alinhado ao nível do time (ex.: "vamos enquadrar o problema juntos" ou "quer que eu puxe um panorama dos dados pra começar?").
4. Lembre que pra apresentação final há as skills `consulting-storytelling` e `azzas-identidade-visual`.

Mantenha o que aprendeu (pilar, nível técnico, objetivo) em mente durante toda a sessão.
