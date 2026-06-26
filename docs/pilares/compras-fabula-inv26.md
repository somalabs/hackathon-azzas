# Hackathon — Desafio: Distribuição Inicial de Coleção

**Marca:** Fábula · **Coleção:** Inverno 2026 (INV26) · **Tribo Plan & DS · Azzas 2154**

> Versão legível do briefing. O documento original (`.docx`) e o deck (`.pptx`) estão nesta pasta.

## 1. Contexto do desafio

A Fábula é uma marca infantil do grupo Azzas 2154. A cada coleção, o Planejamento faz a
**distribuição inicial** dos produtos comprados entre as filiais físicas, antes que o
ressuprimento automático assuma o abastecimento contínuo. O desafio: criar um algoritmo/solução
que automatize e otimize essa distribuição inicial para a INV26. (Coleção passada de propósito,
para permitir comparar resultados.)

**1.1 Por que importa** — o ressuprimento automático reabastece por histórico de vendas e precisa
de **≥14 dias** de venda em loja para calibrar. Durante esse aquecimento, cada loja depende só do
estoque recebido na distribuição inicial. Pouco → ruptura; demais → estoque parado.

**1.2 Fluxo do estoque** — todo o estoque comprado está no CD. O que não for distribuído fica como
**Estoque Regulador** (fonte do ressuprimento). Não há volume além do comprado. Otimizar a
distribuição inicial é também otimizar o regulador.

## 2. Objetivo

Algoritmo de distribuição inicial que: garanta cobertura de **(14 + leadtime)** dias por filial
que receber o produto; respeite o sortimento (NÃO = não enviar); opere dentro do estoque comprado;
priorize filiais estratégicas quando faltar estoque; e decida sobre completude de grade (se não dá
pra montar exposição coerente, melhor não enviar).

## 3. Escopo e restrições

- **No escopo:** filiais físicas da Fábula (**10 lojas**); todos os produtos INV26 do arquivo de compra; output no grão **filial × produto × cor × tamanho**.
- **Fora:** e-commerce (`FABULA ECOMMERCE CM`, `FABULA ECOMMERCE SP CM`) — ignore; ressuprimento futuro; precificação/markdown.
- **Restrição de data:** lançamento oficial era 26/02/2026; data-base de referência **31/03/2026**. ⚠️ Nenhum dado posterior a 31/03/2026 pode ser usado (vazamento / irreprodutibilidade).

## 4. Arquivos fornecidos

**`compra_INV26_lancamento_fabula.xlsx`** — o que foi comprado (volume disponível).
`PRODUTO`, `COR_PRODUTO`, `DESCRICAO`, `COMPRA` (total produto-cor), `TAM_1`…`TAM_6` (qtd por
posição de grade; 0 = tamanho inexistente). 298 produto-cor, **57.112 peças** (220 com 4 tamanhos, 52 com 5, 21 com 3).

**`sortimento_INV26_lancamento_fabula.xlsx`** — quais produto-cor podem ir p/ cada filial.
`FILIAL`, `PRODUTO`, `COR_PRODUTO`, `SORTIMENTO` (SIM/NÃO). NÃO = proibido; SIM = permitido (não
obriga). 49 de 2.980 combinações são "NÃO". (O time pode propor nova clusterização, com racional.)

**`leadtimes_INV26_lancamento_fabula.xlsx`** — dias de trânsito CD → filial. `FILIAL`, `LEADTIME`.

> 📦 Os três arquivos `.xlsx` contêm dados comerciais granulares e **não estão versionados** neste
> repositório público — são entregues aos times do pilar Compras separadamente.

| Filial | Leadtime (dias) |
|---|---|
| FABULA SHOP LEBLON CM | 4 |
| FABULA RDB CM | 4 |
| FABULA BARRA SHOPPING | 4 |
| FABULA ELDORADO CM | 6 |
| FABULA RIO SUL CM | 4 |
| FABULA BARRA SALVADOR CM | 16 |
| FABULA HARMONIA SP CM | 6 |
| FABULA PLAZA SHOP CM | 4 |
| FABULA SHOP VITORIA CM | 11 |
| FABULA CENTRO CM | 4 |

## 5. Acesso ao banco de dados

Além dos arquivos, o time acessa o banco da Azzas via **MCP no Claude** (histórico de vendas,
estoque, cadastro de produto). Sem restrição de tabelas — exceto a data-base (31/03/2026).

## 6. Regras de negócio obrigatórias (hard constraints)

1. **Sortimento:** produto-cor com `NÃO` → zero unidades p/ a filial, em qualquer tamanho.
2. **Estoque comprado:** soma distribuída por produto-cor-tamanho ≤ `TAM_N`. Inteiros não-negativos.
3. **Mínimo por SKU:** se enviar, ≥ 1 unidade.
4. **Completude de grade:** o time define o limiar para enviar grade incompleta.
5. **Exclusão de e-commerce:** nenhuma unidade p/ canais de e-commerce.

## 7. Decisões em aberto (o time decide e justifica)

- **7.1 Estimativa de demanda** — proxy histórico (similares/categoria/sazonalidade), granularidade, produtos sem análogo.
- **7.2 Priorização de filiais** — volume/faturamento, perfil de produto, geografia, ponderação. (Não há clusterização oficial.)
- **7.3 Priorização dentro da grade** — quando falta um tamanho, qual filial leva.
- **7.4 Limiar de completude de grade** — % mínimo de tamanhos, nº mínimo, etc.

## 8. Output esperado

Tabela: `FILIAL` · `PRODUTO` · `COR_PRODUTO` · `TAMANHO` (1–6) · `QTD_DISTRIBUIR` (≥1).
Linhas com 0 são omitidas. **Validações:** sem violação de sortimento; soma ≤ estoque comprado por
produto-cor-tamanho; sem e-commerce; inteiros ≥ 1.

**Entregáveis adicionais:** código/plataforma reprodutível; arquivo de output; documentação das
decisões (seção 7) com justificativa em dados; análise de cobertura por filial.

## 9. Critérios de avaliação

| Critério | O que avalia | Peso |
|---|---|---|
| Cobertura de demanda | % filial-produto que atinge (14+leadtime) dias sem ruptura | Alto |
| Eficiência do estoque | % distribuído vs. retido no regulador sem necessidade | Alto |
| Respeito às restrições duras | Zero violações de sortimento/estoque/integridade | **Eliminatório** |
| Qualidade da decisão sobre grade | Coerência do limiar e impacto na cobertura | Médio |
| Fundamentação das decisões | Justificativa baseada em dados (seção 7) | Médio |
| Reprodutibilidade | Roda sem intervenção, mesmo resultado, sem dados INV26 pós-data-base | Alto |

## 10. Glossário

**SKU** = produto + cor + tamanho · **Produto-cor** = produto + cor (sem tamanho) ·
**Distribuição inicial** = envio do CD para filiais no lançamento · **Estoque Regulador** = saldo
no CD após distribuição (alimenta o ressuprimento) · **Ressuprimento automático** = reposição por
histórico, após 14 dias · **Leadtime** = dias de trânsito CD→filial · **Horizonte de cobertura** =
14 + leadtime · **Grade** = tamanhos ativos de um produto-cor · **Ruptura** = falta de estoque com
demanda · **CD** = Centro de Distribuição.
