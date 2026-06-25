# Azzas MCP — Referência detalhada dos agentes

> Tabelas listadas aqui são as expostas pelo índice de cada agente. Use sempre
> `<agente>__describe_table(<tabela>)` para o schema real e `get_business_rules()` para o SQL
> canônico antes de montar queries não-triviais. Nomes podem mudar; confirme via `get_context`.

## Regras de PII (valem para TODOS os agentes — prioridade máxima)

Nunca colocar no SELECT nem materializar: CPF/RG/passaporte, nome completo, e-mail, telefone,
endereço, **ID de cliente individual** (mesmo que só um número), matrícula de funcionário,
dados de cartão, IP/device/cookie, e **combinações reidentificadoras** (ex.: filial + data +
valor exato). `LIMIT` não resolve. Sempre agregar por dimensão de negócio. Pedido que exige
PII → recusar e oferecer alternativa agregada. Atenção redobrada em `publicar_dashboard` (os
recordsets viram Parquet em blob público).

**Colunas PII conhecidas:** `ClienteIdDia` (=CPF, em `clientes` janela 12m), `cpf`/`cpf_cliente`,
`ClienteID` (clusterização McKinsey), `buyer_email`, `shopper_email`. Comentários de cliente
(`return_comment`, `csat_feedback`, `shopper_message`) só de forma agregada/por tema, nunca verbatim.

---

## `vendas_linx` — Vendas BR (Linx) · Varejo + Digital
Marcas: FARM, Animale, Fábula, NV, Maria Filó, Foxton, Cris Barros, Carol Bassi (Reserva chegando).

- **Métrica base:** `VALOR_PAGO_PROD` (líquida); `VALOR_PROD` = bruto.
- **Canal:** `TIPO_VENDA` → Varejo `VENDA_LOJA`; Digital `VENDA_ECOM`/`VENDA_OMNI`/`VENDA_VITRINE`.
- **KPIs:** Markup = Σvalor_pago/Σcmv_liquido · Ticket = Σvalor_pago/COUNT(DISTINCT chave_pedido) · PA = Σqtd/pedidos · Margem = (líquida−cmv)/líquida · Desconto = (bruto−líquido)/bruto.
- **Visão faturada × captada** (exclusivo): perguntar na 1ª pergunta de venda; default faturada.
- **Casos que exigem `get_business_rules`:** correção de sinal do CMV, fase Sale/Off/Coleção, SSS/Loja Nova.
- **Tabelas:** `TB_WANMTP_VENDAS_LOJA_CAPTADO` (fato), `PRODUTOS`, `PRODUTOS_PRECOS`, `PRODUTO_CORES`, `PRODUTOS_TAMANHOS`, `LOJAS_REDE`, `FILIAIS`, `LOJAS_PREVISAO_VENDAS`, `ANMN_ESTOQUE_HISTORICO_PROD`, `ANMN_ESTOQUE_HISTORICO_PROD_GRADE`, `DATA_OFF`, `cd_loja`, `bq_audit`.

## `clientes` — Base de Clientes
- **Duas perspectivas (declarar sempre, não são comparáveis 1:1):** "Ano de competência" (`acomp_clientes_base`) vs "Janela móvel 12m" (`crm_clientes_tabela1`, ~9 GB).
- **Árvore lógica:** Receita = Qtde Clientes × VA · VA = TM × Freq · TM = PA × PM · Clientes = Novo + Retido + Reativado.
- **Filtros padrão:** `marca IS NOT NULL AND marca <> ''`, `tipo_canal='canal entrada'`, filtro de `ano`. Multicanal → dividir contagem por 2 (ou 3 c/ franquia). Contagem = `SUM(qtde_cli_1a_compra_ano)`.
- **Pegadinha janela 12m:** só `Clientes Base Ativa` usa janela 12m; aplicar `WHERE Data BETWEEN <12m>` em tudo infla receita 100–2000×. Marcas com acento → usar `LIKE` (`'Maria Fil%'`, `'F_bula'`).
- **`ClienteIdDia` = CPF** → só em agregação.
- **Tabelas:** `acomp_clientes_base`, `crm_clientes_tabela1`, `tipo_canal`, `marca`/`Marca`, `TipoCliente`, `pedido`, `cliente` (PII), `filial`, `colecao`, `lovable_vendas_clientes`, `lovable_vendas_midia`.

## `devolucoes` — Trocas e Devoluções BR (9 marcas)
- **Fato único:** `trusted_troque_devolucao`.
- **Filtros críticos obrigatórios:** `LOWER(status)=LOWER(ultimo_status)`, `ultimo_status<>'cancelado'`, `rede_lojas` sempre especificado, janela de `data_solicitacao`.
- **Escopo a confirmar:** marca (`rede_lojas`; ex.: BYNV=16), tipo de reversa, período (default 30d).
- `cpf_cliente` = PII. Devolução de atacado mora em `info_devolucao_v2` (outro agente), não reconciliar.
- **Dimensões:** `rede_lojas`, `marca`, `tipo_reversa`, `cod_cor`, `tamanho`, `ref_id_produto`, `motivo`.

## `ciclo_de_venda_atacado` — Atacado / B2B marcas BR
Marcas: ANIMALE(+JEANS), FARM(+ETC), FABULA, FOXTON, MARIA FILÓ, OFF PREMIUM, RESERVA. (BYNV ausente.)
- **Venda padrão** = `VENDA_ORIGINAL` (>0); `TIPO_VENDA IN ('VENDA','PRE VENDA')`. Filtrar sempre por `COLECAO`.
- **Markup realizado** = Σ(VENDA_ORIGINAL×markup)/Σ(VENDA_ORIGINAL). Atingimento = SUM(VENDA_ORIGINAL)/MAX(META).
- **Coleções:** VER/AV/INV/AI + ano (ex.: `INV26`). "Coleção atual" via CTE canônica (`Posicao=1`).
- **Joins:** clientes/financeiro/Somaplace por `CLIFOR+MARCA`; produto por `PRODUTO+COR_PRODUTO`.
- **Tabelas (22):** `info_venda` (fato), `info_cancelamento`, `info_fat_nf`, `info_embalado`, `info_devolucao_v2`, `info_metas`, `dim_clientes_v2`, `info_produto_v2`, `produtos_colecao`, `programacao`, `info_financeira`, `historico_bloqueio`, `cadastro_somaplace_v2`, `venda_somaplace_v2`, `afiliados_multimarca`, `afiliados_venda_v2` (única fonte de OFF PREMIUM), `afiliados_vendedores`, `metas_projetos_digitais`, `info_ecommerce`, `prateleira_infinita`, `cessao_varejo`, `soma_online_refined`.

## `midia_e_crm` — Mídia & CRM
- **Mídia paga:** GA4 (`app_web_veiculos`) + GA3 (`app_web_pmax_veiculos`); cruzar período de migração com `UNION ALL`. Custo em USD → `Cost_BRL = Cost_USD × cotacao × fator_marca`. ROAS = Σreceita/Σinvestimento (exibir "ROAS 4,3", sem %).
- **CRM:** Open Rate, CTR, CTOR, Taxa Conv, Ticket. Share CRM = Receita_CRM/Receita_Total (receita **atribuída**; total vem de `vendas_linx`). ROI por canal = Receita_CRM/Investimento.
- **Segmentação McKinsey:** `clusterizacao_mckinsey` (grão por cliente → **agregar por `Cluster`**, 8 clusters).
- **App (Appsflyer, D-2):** `trusted_appsflyer_mau_gran2`/`_gran1`, `trusted_appsflyer_dau`, instalações.
- **Tabelas (25):** mídia (`app_web_veiculos`, `app_web_pmax_veiculos`, `origem_midia`, `cotacao_dolar_diaria`, `comissao_midia`, `trusted_adcost_extra`, `raw_mf_manuais_*`), CRM (`receita_liquida_crm`, `perf_crm_veiculos_prov`, `perf_crm_GA`, `dados_push_dito`, `dash_crm_lovable_omnichat_campanha`, `acomp_agenda`), base (`acomp_clientes_base`, `clusterizacao_mckinsey`, `cliente`(PII), `refined_vendas_mestre`(PII)), app (Appsflyer), Insider (`refined_email_insider`, `refined_mobileapp_insider`, `refined_web_push_insider`).

## `farm_global` — Farm Global US/EU/UK · Varejo + Digital (DTC)
- **Multi-moeda:** receita na moeda nativa do site (`SUM(vl_price_paid × nr_quantity)`); região via `dm_type_sales.st_region`. Converter via `ft_cotacoes` só ao consolidar multi-site → BRL. Default sem escopo = US$.
- **Canal de venda:** `st_channel` STORE/CONCESSION = varejo; ONLINE = digital. (`dm_canais_ecomm` é marketing, não canal de venda.)
- **Status:** `st_event_status` CAPTURED/FULFILLED = venda; REFUNDED = devolução; CANCELLED = à parte.
- **Faturado oficial:** RLM Invoice Register (`Net_Amount_USD`/`_BRL` com PTAX; `Type='Sales'`, excluir `Channel='INTERCOMPANY'`). Excluir sempre `vl_price_paid=0` e `st_fraud=true`.
- **Tabelas (25):** fatos `ft_sales`, `ft_midia`, `ft_GA_fluxo`, `ft_GA_produto`, `ft_stock_*`, `ft_traffic_stores`, `ft_cs_nps`, `ft_chargebacks`, `ft_cluster`, `ft_cotacoes`; dims `dm_sales`, `dm_customers`(PII), `dm_produtos`, `dm_type_sales`, `dm_crm_campaigns`, `dm_canais_ecomm`; RLM (`RLM_Invoice_Register...`, `rlm_inventory_full_view_vs` ~102 GB, `rlm_products`); fotos `aux_style_imagem`/`dim_shopify_pictures`.

## `farm_global_atacado` — Wholesale internacional Farm
- **Duas visões que nunca se somam:** Sell-in (Joor, `joor_sell_in`) vs Faturado wholesale (RLM Invoice Register).
- **"Verba" = faturado a MSRP:** `SUM(Units_Sold × retail_price)`; MSRP de `rlm_products` (join `Company+Style`). Cadastro só tem Company 1 → verba US/UK/EU subestimada (rotular 🔶).
- Multi-moeda (nunca somar moedas nativas). `buyer_email`/`Customer*` = PII.
- **Tabelas:** `joor_sell_in`, `rlm_sales_order_inquiry_bi`, `RLM_Invoice_Register...`, `TB_RLM_Invoice_Register_By_Customer_com_PTAX` (única com Season/Style/Units), `rlm_products`, `dim_shopify_pictures`.

## `farm_global_devolucao` — Devoluções Farm Global (qualitativo)
- Foca em **por que** devolveu (motivos, temas, CSAT). Não cobre taxa quantitativa (isso é `farm_global`).
- **Grão por fonte:** `dim_return_reasons` (primária, event-grained → `COUNT(DISTINCT origin_return_id)`); `loop_returns_line_items` (CDC → dedup com QUALIFY ROW_NUMBER); `returnly_us_line_items` (legado, congelado out/2023).
- Nunca somar cross-plataforma. Comentários de cliente só agregados/por tema, nunca verbatim. CSAT = distribuição, nunca feedback individual.
- **Tabelas:** `dim_return_reasons`, `loop_returns_line_items`, `returnly_us_line_items`, `dim_refunds`, `rlm_returns_authorization_receipts`, `dim_shopify_pictures`.
