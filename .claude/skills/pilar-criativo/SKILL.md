---
name: pilar-criativo
description: >
  Guia do pilar CRIATIVO do Hackathon Azzas. Use quando o time estiver trabalhando no case
  criativo: construir uma coleção cápsula (até 30 produtos) com briefing/tema, produtos, ficha
  de repasse simplificada e produção de moda para showroom. Acione em conversas sobre coleção
  cápsula, briefing de moda, criação de produto, estampa, geração de imagem de produto com IA
  (Freepik, Nano Banana, Flux Kontext Pro), ficha de repasse ou showroom.
---

# Pilar Criativo — Coleção Cápsula com IA

## O case

> **Construir uma coleção cápsula de até 30 produtos**, incluindo: **briefing/tema**,
> **produtos**, **ficha de repasse (simplificada)** e **produção de moda para showroom.**

A pergunta de fundo: como a **criação de imagens com IA** pode ser estratégica para o negócio
— acelerando do croqui ao cadastro, gerando variações de cor/estampa/forma e visualizando
peças na modelo sem produção física.

## Entregável esperado

1. **Briefing / tema** — o conceito da cápsula: inspiração, paleta, público, ocasião, marca de referência.
2. **Produtos** — até 30 peças, com imagens (geradas via IA), categorias e variações.
3. **Ficha de repasse simplificada** — a ponte do criativo para o comercial: por produto, os
   atributos essenciais (categoria, cor/estampa, material, silhueta, faixa de preço sugerida).
4. **Produção de moda para showroom** — visualização das peças (still e/ou na modelo) e a
   narrativa de apresentação da coleção.

## Como o Claude ajuda

- **Briefing & tema:** brainstorming de conceito, coerência com a identidade da marca
  (use a skill `azzas-contexto-publico` para tom/posicionamento), estrutura do storytelling.
- **Curadoria & organização:** montar a grade de produtos (mix de categorias), nomear peças,
  organizar a ficha de repasse como tabela.
- **Geração de imagem:** o time gera as imagens no **Freepik** (modelos Nano Banana, Flux
  Kontext Pro, GPT Image High). O Claude ajuda a **escrever e refinar os prompts** — veja a
  biblioteca em `references/prompts-imagem.md`.
- **Showroom & deck:** com a skill `consulting-storytelling`, montar a apresentação da coleção.

## Toolkit de geração de imagem (do workshop SomaLabs)

Modelos (no Freepik):
- **Nano Banana** — principal: remix, blend, variações, inserção, style.
- **Flux Kontext Pro** — detalhamento: sketches técnicos, vistas, close-ups.
- **GPT Image High** — criativo: tecidos manuais, bordados, display.

Estrutura de prompt: **[VERBO] + [O QUÊ] + de @IMG1 + em @IMG2**.
Verbos úteis: EXTRACT · CONVERT · GENERATE · CHANGE · TURN · INSERT · TRANSFER · INSPIRED BY.
Aspect ratio: 3:4 produto · 9:16 look · 2:3 vistas · 1:1 detalhe. **Sempre rode 4 variações antes de escolher.**

Fluxo criativo do workshop: **EXPLORE** (real → desenho técnico / remix / blend) →
**EXTRACT** (peça → still, vistas, detalhes) → **VARIATIONS** (cor, forma, material) →
**INSERT + STYLE** (inserir tecido/detalhe/estampa, transferir estilo, peça na modelo).

A biblioteca completa de prompts está em **`references/prompts-imagem.md`**. O playbook visual
original é o PDF `[Farm BR] Workshop IA - Assistentes de Estilo.pdf` na raiz do repo.

## Dicas

- Comece pelo **tema** — ele amarra paleta, materiais e silhuetas. Sem tema, a cápsula vira lista de peças soltas.
- Mantenha **coerência visual**: mesma direção de still/fundo para todas as peças facilita o showroom.
- A **ficha de repasse** é o que torna a cápsula "executável" — capriche nos atributos que o comercial precisa.
