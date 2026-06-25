# Onboarding — Hackathon Azzas

Bem-vindo! Este guia coloca seu time pronto pra começar em poucos minutos.

## 1. O que é o hackathon

16 times, 4 pilares estratégicos de IA. Seu time pega **um pilar** e entrega uma solução usando
o **Claude** + o **MCP de dados Azzas**. No fim, todos apresentam.

| Pilar | Case |
|---|---|
| **Criativo** | Coleção cápsula de até 30 produtos (briefing/tema, produtos, ficha de repasse simplificada, produção para showroom). |
| **Compras** | Distribuição de peças da Fábula para a coleção INV26. |
| **Eficiência Operacional** | Automatizar um fluxo operacional do dia a dia (chamados, Feedz, PPT...). |
| **Receita & Clientes** | Nova forma de segmentar a base de clientes para achar oportunidades. |

Detalhes de cada pilar: [`docs/pilares/`](../pilares/). Eles também viram **skills** que o Claude
ativa sozinho quando você fala do tema.

## 2. Pré-requisitos

- **Claude Code** instalado (CLI, app desktop, ou extensão de IDE). Veja `claude.ai/code`.
- Acesso ao **MCP de dados Azzas** (passo 4).
- Git, para clonar este repositório.

## 3. Clonar e abrir

```bash
git clone https://github.com/somalabs/hackathon-azzas.git
cd hackathon-azzas
claude   # abre o Claude Code neste diretório
```

Ao abrir aqui, o Claude **já carrega automaticamente**:
- As **instruções do projeto** (`CLAUDE.md`) — regras do jogo, PII, pilares.
- O **set de skills** (`.claude/skills/`) — guias de dados, pilares, storytelling.

> Confirme dizendo ao Claude: *"quais skills você tem disponíveis?"* — ele deve listar
> `azzas-dados`, `azzas-contexto-publico`, `consulting-storytelling` e as `pilar-*`.

## 4. Conectar o MCP de dados

O MCP dá ao Claude acesso de **leitura** aos dados do grupo (BigQuery) via agentes especializados,
**sempre com proteção de dados pessoais**.

> 🔧 **Configuração:** _(a ser preenchida com o endpoint/config oficial do MCP — ver nota da organização)._
> Quando disponível, o repositório trará um `.mcp.json` e o Claude conectará automaticamente ao
> abrir o projeto. Enquanto isso, use o passo manual abaixo.

**Conexão manual (fallback):**
- No Claude Code: `claude mcp add` e siga o fluxo de autenticação do conector Azzas; ou
- No claude.ai: adicione o conector "Azzas MCP" nas integrações.

Teste pedindo ao Claude: *"faça um ping no agente de vendas do MCP"*.

## 5. Regras do jogo (importantes)

1. **Dados pessoais nunca aparecem.** Nada de CPF, nome, e-mail, ID de cliente individual. Só
   dados **agregados**. Os agentes já recusam — não tente contornar.
2. **Não inventar números.** Todo dado vem do MCP nesta sessão ou de você. Sem dado → "não tenho".
3. **Para venda/receita:** o Claude vai perguntar **canal + marca** antes de puxar número. É de propósito.
4. **Comparações são vs. ano anterior (LY).**
5. **Este repo é público.** Nunca commite dados confidenciais ou sensíveis aqui.

## 6. Fluxo de trabalho sugerido

1. Leia o guia do seu pilar em [`docs/pilares/`](../pilares/) (ou só comece a conversar — a skill ativa).
2. Peça ao Claude para te ajudar a **enquadrar o problema** antes de sair puxando dado.
3. Explore os dados com o MCP (a skill `azzas-dados` orienta o Claude no caminho certo).
4. Construa o entregável. Para a **apresentação final**, peça ajuda da skill `consulting-storytelling`.

## 7. Referências

- [Referência completa do MCP de dados](../recursos/mcp-dados.md)
- [Guias dos pilares](../pilares/)
- Playbook criativo (geração de imagem): PDF na raiz do repositório.
