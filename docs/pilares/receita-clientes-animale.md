# Hackathon: Segmentação de Clientes Animale
**Azzas 2154 · Digital & Data · Pilar Receita & Cliente**

---

## O Desafio

> **Propor novas formas de segmentar a base de clientes da Animale. Agrupe os clientes da melhor forma para encontrar insights e oportunidades de negócio.**

O objetivo é ir além dos modelos existentes. Analise padrões de compra, proponha uma nova dimensão de agrupamento e conecte o resultado a uma alavanca de negócio real.

---

## Modelos de Segmentação Atuais

### 1. RFM

Classifica clientes por três dimensões comportamentais de compra:

| Dimensão | Definição |
|---|---|
| **R — Recência** | Quantos dias desde a última compra |
| **F — Frequência** | Número de transações realizadas na marca |
| **M — Monetary** | Valor acumulado gerado pelo cliente |

**Segmentos resultantes:** Champions · Loyal Customers · Potential Loyalist · Need Attention · At Risk · Can't Lose Them · Hibernating · Recent Customers

---

### 2. Matriz McKinsey: Valor × Frequência

| | **- Valor** | **+ Valor** |
|---|---|---|
| **+ Frequência** | Alta freq / Baixo Valor — Ama a marca, mas pode não ter poder aquisitivo para peças maiores | Alta freq / Alto Valor — Clientes fiéis de alto valor. Balizas do que funciona para a marca |
| **- Frequência** | Baixa freq / Baixo Valor — Baixo envolvimento. Experimentadoras ou desengajadas | Baixa freq / Alto Valor — Compras pontuais de alto valor. Analisar categorias e sazonalidade |

**Segmentos complementares:**
- **Compra Única** — Clientes de uma só compra. Chave para entender sazonalidade e o que as faria voltar.
- **Top Clientes** — Maiores consumidoras hoje. DNA da marca. Referência para atrair novas clientes.

---

### 3. Nobres & Liquideiros *(modelo emergente)*

Segmentação por **comportamento de preço** — o quanto a cliente compra a preço cheio vs. com desconto.

| Perfil | Regra | Leitura |
|---|---|---|
| **Nobre** | Desconto médio **≤ 20%** nas compras na marca | Sinalizadoras de valor de marca. Dispostas a pagar o preço justo. |
| **Liquideiro** | Desconto médio **> 20%** nas compras na marca | Sensíveis a preço. Ativadas por campanhas e liquidações. |

> ⚡ Modelo recente, ainda sendo validado — ideal para testar hipóteses cruzadas com outros critérios de segmentação.

---

## O que RFM e a Matriz McKinsey não enxergam?

Estes são ângulos que os modelos atuais não capturam e que podem revelar oportunidades reais:

- **Canal preferencial** — App, site desktop, loja física. O comportamento muda por canal? Clientes de app têm perfil de compra diferente?
- **Ciclo de vida da moda** — A cliente compra no lançamento ou no fim da curva? Compra básicos ou peças de destaque de coleção?
- **Estilo & categorias** — Existe uma "cliente de vestido" vs. "cliente de calça"? Clusters de categoria se mantêm consistentes ao longo do tempo?
- **Risco de churn** — Quais segmentos têm maior propensão ao abandono? Quais têm maior potencial de upgrade ou reativação?

> Seu papel no hackathon é propor e testar um desses ângulos — ou outro que você enxergar nos dados.

---

## Dados Disponíveis: Claude + MCP

O **MCP IAZZAS** conecta o Claude diretamente ao BigQuery da Azzas. Você acessa dados reais de clientes da Animale fazendo perguntas em linguagem natural — **sem precisar escrever SQL**.

**Como usar:**

1. Abra o Claude (claude.ai) e certifique-se de que o **MCP IAZZAS** está ativo no menu de ferramentas.
2. Faça perguntas sobre clientes da Animale em português. O Claude traduz para SQL e retorna os dados.
3. Peça análises, tabelas, gráficos ou comparações — o Claude processa e apresenta os resultados.
4. Itere: refine a pergunta, filtre por período, segmento ou canal até chegar ao insight.

---

## O Que Entregar

Sua proposta de segmentação deve cobrir os quatro componentes:

| # | Componente | O que responder |
|---|---|---|
| **01** | **A Segmentação** | Qual a lógica de agrupamento? Quais variáveis você usa, quantos segmentos e como cada um é caracterizado? |
| **02** | **O Tamanho da Base** | Quantas clientes cabem em cada segmento? Qual o peso financeiro (receita) de cada grupo? |
| **03** | **O Insight** | O que esse novo olhar revela que RFM ou a Matriz não enxergavam? Qual é a descoberta mais relevante? |
| **04** | **A Alavanca** | Qual ação de negócio esse segmento habilita? Campanha, produto, canal, oferta — seja específico. |

> Formato livre — slides, nota, planilha ou apresentação oral. O que importa é a clareza do raciocínio.
