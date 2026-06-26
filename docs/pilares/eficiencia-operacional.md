# Hackathon — Eficiência Operacional

**Mão na massa com Automação + IA · Azzas 2154**

> Versão legível do deck do participante. O original interativo está em `eficiencia-operacional.html`.

Hoje você vai construir o seu **primeiro agente de IA**. Não precisa ser técnico — vamos
transformar tarefas manuais em fluxos inteligentes e fazer a tecnologia trabalhar por você.

## 1. O que é automação?

Fazer o computador executar tarefas repetitivas sozinho, seguindo regras — sem clicar, copiar e
colar. Como uma máquina de lavar: aperta o botão e ela faz o trabalho chato, sempre igual. No
escritório: relatórios, e-mails, planilhas.

- **Repetitiva** — tarefas que se repetem do mesmo jeito.
- **Baseada em regras** — "se isso, faça aquilo". Sem improviso.
- **Sem parar** — 24/7, rápido e sem erro de digitação.

## 2. Automação × Automação com IA

| Automação tradicional | Automação com IA |
|---|---|
| Segue regras fixas, passo a passo | Entende, interpreta e decide |
| Trava quando aparece algo fora do padrão | Lida com o inesperado |
| Ex.: mover um anexo para uma pasta | Ex.: ler um e-mail, entender o pedido e responder |

A automação **faz**. A IA **entende**. Juntas, resolvem o que antes exigia uma pessoa.

## 3. As ferramentas

- **Claude — o cérebro de IA.** Lê & resume (documentos, planilhas, e-mails), escreve, analisa
  dados e gera código/páginas. Um estagiário brilhante que nunca cansa.
- **Prompt — a instrução.** Seu pedido para a IA. **Papel + tarefa + dados + formato = resultado
  certeiro.**
  - ❌ Fraco: *"Analise as vendas"* — vago, sem recorte/formato/objetivo.
  - ✅ Forte: *"Você é um analista. Calcule vendas e MKP por marca, região e estado a partir deste
    CSV e liste 3 destaques em 5 linhas."*
- **N8N — os braços que conectam tudo.** Ferramenta visual de automação (blocos tipo Lego) que
  liga apps sem programar do zero. Fluxo: **Gatilho** (horário/arquivo/clique) → **Conectores**
  (e-mail, Teams, Drive, bancos) → **Nó de IA** (Claude) → **Saídas** (enviar/publicar/salvar/avisar).

**Prompt + Claude + N8N = Agente** que resolve a missão.

## 4. O desafio

> **Crie um agente de análise de dados.** A partir de uma base, o agente gera uma visão e comunica
> os resultados automaticamente.

1. **Ler a base** — acessa os dados e entende a estrutura.
2. **Gerar a visão** — analisa e produz os principais números, recortes e insights.
3. **Comunicar** — envia os resultados sozinho, por e-mail, Teams ou um painel.

**Formato:** em equipes · 2h15 de execução · 3 entregáveis · apresentação final.

## Acesso aos dados

A base pode ser o **MCP de dados Azzas** (via Claude) ou uma base própria do time (CSV/planilha).
Mantenha **PII fora** de qualquer saída — ver [regras do jogo](../onboarding/README.md#5-regras-do-jogo-importantes)
e a skill `azzas-dados`.
