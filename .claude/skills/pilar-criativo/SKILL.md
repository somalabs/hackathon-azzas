---
name: pilar-criativo
description: >
  Guia do pilar CRIATIVO do Hackathon Azzas. Use quando o time estiver criando uma coleção
  cápsula (até 30 produtos) com IA: partindo das próprias referências, fazendo combinados e
  gerando as imagens dos produtos no Freepik. Acione em conversas sobre coleção cápsula, briefing
  de moda, referências/inspiração, tema, estampa, geração de imagem de produto com IA (Freepik,
  Nano Banana, Flux Kontext Pro), ou como apresentar a coleção.
---

# Pilar Criativo — Coleção Cápsula com IA

## O case

> **Criar uma coleção cápsula (até 30 produtos) usando IA** — e pensar como apresentá-la.

Não há um briefing fechado: a essência do desafio é o time **trazer as próprias referências**,
fazer **combinados** entre elas e **criar a coleção**. A criação das imagens dos produtos é feita
no **Freepik**. O foco é explorar como a geração de imagem com IA acelera o trabalho criativo —
do conceito à visualização — sem produção física.

## O caminho (leve, o time conduz)

1. **Reúna referências** — as suas, do seu repertório/inspiração. É daqui que a coleção nasce.
2. **Combine** — misture referências, cores, estampas, materiais e formas até achar a direção.
3. **Crie a coleção** — até 30 produtos coerentes entre si. Gere as imagens no Freepik.
4. **Pense na apresentação** — como contar a história da coleção (use `consulting-storytelling`).

## Adicionais opcionais (se o time quiser ir além)

Nada disso é obrigatório — são formas de enriquecer a coleção com dados:

- **Tendências** — pesquisar referências e tendências de mercado para embasar o tema.
- **Análise de venda** — via MCP (skill `azzas-dados`), olhar o que vende/girou em coleções
  passadas (ex.: categorias, cores) para inspirar escolhas. Sempre agregado.
- **Ficha de repasse simplificada** — organizar os produtos numa tabela com os atributos
  essenciais (categoria, cor/estampa, material, silhueta) — útil pra "passar" a coleção adiante.

## Como o Claude ajuda

- **Conceito & curadoria:** brainstorming de tema a partir das suas referências, coerência da
  cápsula, nomes de peças, organização da grade de produtos.
- **Prompts de imagem:** o time gera as imagens no **Freepik**; o Claude ajuda a escrever e
  refinar os prompts. Biblioteca pronta em **`references/prompts-imagem.md`**.
- **Apresentação:** com `consulting-storytelling` e `azzas-identidade-visual`, montar o showroom/deck.

## Toolkit de imagem (Freepik) — resumo

Modelos: **Nano Banana** (remix, blend, variações, inserção, style — principal) · **Flux Kontext
Pro** (sketches técnicos, vistas, close-ups) · **GPT Image High** (tecidos, bordados, display).
Estrutura de prompt: **[VERBO] + [O QUÊ] + de @IMG1 + em @IMG2**. Aspect ratio: 3:4 produto · 9:16
look · 1:1 detalhe. Sempre rode 4 variações. Fluxo: EXPLORE → EXTRACT → VARIATIONS → INSERT+STYLE.

A biblioteca completa de prompts está em **`references/prompts-imagem.md`**. O material original é o
PDF `[Farm BR] Workshop IA - Assistentes de Estilo.pdf` (workshop SomaLabs).

## Dicas

- A coleção é sua — **comece pelas suas referências**, não por uma fórmula.
- Coerência visual ajuda no showroom: mantenha uma direção consistente de still/fundo.
- Rode várias variações no Freepik e **cure** as melhores; a IA é rápida pra explorar.
