# Briefing — Aplicação MVP de Distribuição (Fábula INV26)

> **Para usar:** na sessão onde você está montando o algoritmo de distribuição, cole o
> prompt do final ("Prompt pronto pra colar"). Os dados (output do algoritmo) já estão
> nessa sessão — esta app só os lê e apresenta. Este arquivo registra as decisões fechadas
> para que a app saia pronta de uma vez.

---

## O que é

Aplicação **web de página única (SPA), 100% estática** (HTML + CSS + JS puro, sem backend),
para uma **apresentação de MVP** do case de Compras. Ela exibe a distribuição inicial da
coleção **INV26 da Fábula** entre as **10 lojas físicas** que o algoritmo gerou, explica os
critérios usados e permite "gerar os pedidos" (mockado) e exportar para xlsx.

**Por que SPA estático:** roda abrindo o arquivo no navegador, sem servidor para cair durante
a apresentação. Dados embarcados direto no JS (gerados pelo algoritmo nesta mesma sessão).

---

## Decisões fechadas (não reabrir)

| # | Decisão | Escolha |
|---|---|---|
| 1 | Stack / formato | **SPA estático** — HTML+CSS+JS, dados embarcados em um `data.js` ou inline. Sem build, sem backend. |
| 2 | Contrato de dados | **Dispensado** — app construída na mesma sessão do algoritmo; os dados já estão disponíveis e são embarcados direto. |
| 3 | Botão "gerar pedidos" | **100% mockado** — modal/toast de confirmação → "✓ N pedidos gerados no sistema" + download de um arquivo. Sem integração real. |
| 4 | Dashboards | **Todos os 4** (ver seção Dashboards). |
| 5 | Escopo | **Focado em INV26 Fábula / 10 lojas, dados embarcados.** Não precisa aceitar upload nem outras coleções. |

---

## Dados que a app embarca (vindos do algoritmo)

A app consome o que o algoritmo já produziu na sessão. No mínimo:

- **Distribuição** (linha = decisão final): `FILIAL · PRODUTO · COR_PRODUTO · TAMANHO · QTD_DISTRIBUIR`
- **Por produto-cor:** `COMPRA` total, total distribuído, sobra no CD, grade comprada (TAM_1…TAM_6),
  grupo de produto, descrição.
- **Por filial:** leadtime, horizonte (14 + leadtime), velocidade média prevista, demanda prevista,
  qtd recebida, % da demanda atendida, cobertura de grade média.
- **Critérios do modelo:** 6 dimensões de similaridade e pesos (GRUPO 0,35 · preço 0,15 · tecido 0,15
  · manga 0,10 · estampa 0,10 · praia+bebê 0,15), pesos de coleção (INV23=1, INV24=2, INV25=3),
  faixas de preço (T1 <100, T2 100–199, T3 200–299, T4 ≥300), janela on-season 122 dias.
- **Validações:** violações de sortimento (deve ser 0), violações de estoque (0), valores não-inteiros (0),
  e-commerce no output (deve ser ausente).

> Formato técnico (CSV embutido como string, array JS, ou objeto) fica a critério da app —
> como é a mesma sessão, basta serializar os dataframes finais.

---

## Telas / Dashboards (os 4)

**A — Drivers da decisão (como o algoritmo pensou)**
- Pesos das 6 dimensões de similaridade (barra ou donut).
- Faixas de preço e pesos de coleção.
- Velocidade prevista × leadtime × horizonte por filial.
- Card explicando a lógica: "INV26 não tem histórico → mapeamos para os 15 similares de INV23/24/25".

**B — Resultado por loja**
- Tabela/ranking das 10 filiais: demanda prevista, qtd recebida, % atendido, cobertura de grade, leadtime.
- Destaque para filiais críticas de leadtime (**Salvador 30d**, **Vitória 25d**).
- Gráfico de barras de unidades por loja.

**C — Resultado por produto**
- Comprado vs distribuído vs sobra no CD (a maior parte fica no CD para ressuprimento).
- Filtro por grupo de produto.
- Drill: ao abrir um produto-cor, ver a grade distribuída por filial × tamanho.

**D — Saúde / validações da distribuição**
- Semáforo verde: 0 violações de sortimento, 0 de estoque, tudo inteiro, sem e-commerce.
- Lista de alertas, se houver (ex.: filial com grade incompleta).

**+ Tabela detalhada** filtrável (filial, produto, cor, tamanho, qtd) — a base do output.

---

## Botão "Gerar pedidos no sistema" (mockado)

- Posição: topo/header, com selo "requer aprovação do analista".
- Fluxo: clique → modal "Confirmar geração de N pedidos de distribuição para 10 lojas?"
  → confirmar → toast "✓ N pedidos gerados no sistema" + estado visual "Pedidos gerados ✓".
- Sem integração real. Deixar claro na UI que é simulação para o MVP.

---

## Exportação

- Botão **"Exportar xlsx"** que baixa a tabela de distribuição (`FILIAL · PRODUTO · COR_PRODUTO ·
  TAMANHO · QTD_DISTRIBUIR`). Como é SPA estático, usar lib client-side (ex.: SheetJS/xlsx via CDN
  ou embutida) — sem backend.

---

## Identidade visual

Seguir a skill **`azzas-identidade-visual`** (paleta, tipografia, tokens CSS) para a app sair no
padrão da marca. Aparência de produto real, limpa, executiva — é uma apresentação de MVP.

---

## Fora de escopo (não fazer)

- Backend, banco de dados, autenticação.
- Upload de arquivos / suporte a outras coleções ou marcas.
- Integração real com ERP.
- Recalcular o algoritmo no navegador — a app só **exibe** o resultado já calculado.

---

## Prompt pronto pra colar (na sessão do algoritmo)

> Agora construa a aplicação MVP de apresentação seguindo o briefing em
> `HANDOFF_APP_DISTRIBUICAO.md`. É um **SPA estático** (HTML+CSS+JS, sem backend), com os dados
> da distribuição que você já gerou **embarcados** no próprio código. Inclua os 4 dashboards
> (drivers da decisão, resultado por loja, resultado por produto, saúde/validações), a tabela
> detalhada filtrável, o botão **mockado** "Gerar pedidos no sistema" (modal de confirmação +
> toast) e o botão **Exportar xlsx**. Use a skill `azzas-identidade-visual` para o visual.
> Foco em INV26 Fábula / 10 lojas — sem upload e sem outras coleções.
