-- =====================================================
-- PÁGINA HOME (1) - DASHBOARD EXECUTIVO
-- Sistema de Gestão de Mercado - APEX
-- =====================================================
-- Este script cria a página 1 (HOME) com:
-- - 4 Cards de KPI
-- - 3 Gráficos
-- - 2 Alertas (Estoque e Compras)
--
-- ⚠️ IMPORTANTE: Execute este script em:
-- Workspace: MERCADO_FAMILIA
-- Usuário: APEX_DEVELOPER
-- No: SQL Workshop > SQL Commands
-- =====================================================

-- =====================================================
-- QUERIES DE SUPORTE (Crie estas primeiras se necessário)
-- =====================================================

-- View: Dashboard - KPIs
CREATE OR REPLACE VIEW DASHBOARD_KPIS AS
SELECT
  -- KPI 1: Vendas de Hoje
  NVL(SUM(CASE WHEN TRUNC(v.data_venda) = TRUNC(SYSDATE) AND v.status = 'CONCLUIDA'
    THEN v.valor_final ELSE 0 END), 0) as vendas_hoje,
  -- KPI 2: Faturamento do Mês
  NVL(SUM(CASE WHEN TRUNC(v.data_venda, 'MM') = TRUNC(SYSDATE, 'MM') AND v.status = 'CONCLUIDA'
    THEN v.valor_final ELSE 0 END), 0) as faturamento_mes,
  -- KPI 3: Produtos em Falta
  (SELECT COUNT(*) FROM PRODUTOS WHERE quantidade <= estoque_minimo AND ativo = 'S') as produtos_falta,
  -- KPI 4: Clientes Ativos
  (SELECT COUNT(*) FROM CLIENTES WHERE ativo = 'S') as clientes_ativos,
  -- Contexto
  SYSDATE as data_referencia
FROM VENDAS v
GROUP BY SYSDATE;

-- View: Dashboard - Vendas Últimos 7 Dias
CREATE OR REPLACE VIEW DASHBOARD_VENDAS_7DIAS AS
SELECT
  TRUNC(data_venda) as data,
  TO_CHAR(data_venda, 'DD/MM/YYYY') as data_formatada,
  COUNT(DISTINCT venda_id) as qtd_vendas,
  SUM(valor_final) as total_vendido
FROM VENDAS
WHERE data_venda >= TRUNC(SYSDATE) - 7
  AND status = 'CONCLUIDA'
GROUP BY TRUNC(data_venda), TO_CHAR(data_venda, 'DD/MM/YYYY')
ORDER BY data DESC;

-- View: Dashboard - Top 5 Produtos
CREATE OR REPLACE VIEW DASHBOARD_TOP_PRODUTOS AS
SELECT
  p.produto_id,
  p.nome,
  SUM(iv.quantidade) as quantidade_vendida,
  SUM(iv.subtotal) as valor_total
FROM ITENS_VENDA iv
JOIN PRODUTOS p ON iv.produto_id = p.produto_id
WHERE iv.criado_em >= TRUNC(SYSDATE) - 30
GROUP BY p.produto_id, p.nome
ORDER BY quantidade_vendida DESC;

-- View: Dashboard - Formas de Pagamento
CREATE OR REPLACE VIEW DASHBOARD_PAGAMENTOS AS
SELECT
  forma_pagamento,
  COUNT(*) as quantidade,
  SUM(valor_final) as total,
  ROUND(COUNT(*) * 100 / SUM(COUNT(*)) OVER (), 2) as percentual
FROM VENDAS
WHERE status = 'CONCLUIDA'
  AND data_venda >= TRUNC(SYSDATE) - 30
GROUP BY forma_pagamento
ORDER BY total DESC;

-- =====================================================
-- INSTRUÇÕES MANUAIS PARA CRIAR A PÁGINA NO APP BUILDER
-- =====================================================
--
-- Se preferir criar manualmente (RECOMENDADO para primeira página):
--
-- 1. Acesse APEX App Builder
-- 2. Abra sua aplicação
-- 3. Clique em "1" ou "+" para criar página
-- 4. Escolha "Blank Page"
-- 5. Page Number: 1
-- 6. Page Name: HOME
-- 7. Page Title: Home
--
-- 8. ADICIONE REGIÃO 1: KPIs Topo
--    - Type: Static Content
--    - Title: KPIs do Sistema
--
-- 9. ADICIONE ITEMS (nos KPIs):
--    a) P1_VENDAS_HOJE
--       - Type: Value
--       - SQL: SELECT SUM(valor_final) FROM VENDAS
--              WHERE TRUNC(data_venda) = TRUNC(SYSDATE) AND status = 'CONCLUIDA'
--       - Format: Currency
--       - Icon: trending-up
--
--    b) P1_FATURAMENTO_MES
--       - Type: Value
--       - SQL: SELECT SUM(valor_final) FROM VENDAS
--              WHERE TRUNC(data_venda,'MM') = TRUNC(SYSDATE,'MM') AND status = 'CONCLUIDA'
--       - Format: Currency
--       - Icon: bar-chart
--
--    c) P1_PRODUTOS_FALTA
--       - Type: Value
--       - SQL: SELECT COUNT(*) FROM PRODUTOS
--              WHERE quantidade <= estoque_minimo AND ativo = 'S'
--       - Format: Number
--       - Icon: warning-circle
--       - CSS Class: alert-badge
--
--    d) P1_CLIENTES_ATIVOS
--       - Type: Value
--       - SQL: SELECT COUNT(*) FROM CLIENTES WHERE ativo = 'S'
--       - Format: Number
--       - Icon: users
--
-- 10. ADICIONE REGIÃO 2: Gráfico Vendas 7 Dias
--     - Type: Chart
--     - Chart Type: Line
--     - SQL: SELECT * FROM DASHBOARD_VENDAS_7DIAS
--     - Label: data_formatada
--     - Value: total_vendido
--
-- 11. ADICIONE REGIÃO 3: Top 5 Produtos
--     - Type: Chart
--     - Chart Type: Bar (Horizontal)
--     - SQL: SELECT * FROM DASHBOARD_TOP_PRODUTOS WHERE ROWNUM <= 5
--     - Label: nome
--     - Value: quantidade_vendida
--
-- 12. ADICIONE REGIÃO 4: Distribuição de Pagamentos
--     - Type: Chart
--     - Chart Type: Pie
--     - SQL: SELECT * FROM DASHBOARD_PAGAMENTOS
--     - Label: forma_pagamento
--     - Value: quantidade
--
-- 13. ADICIONE REGIÃO 5: Alertas de Estoque
--     - Type: Interactive Grid
--     - SQL: SELECT produto_id, nome, quantidade, estoque_minimo,
--                  CASE WHEN quantidade <= estoque_minimo THEN 'CRÍTICO' ELSE 'BAIXO' END status
--            FROM PRODUTOS WHERE quantidade <= estoque_minimo * 1.5 AND ativo = 'S'
--     - Read Only: Yes
--     - Sort By: quantidade ASC
--
-- 14. ADICIONE REGIÃO 6: Compras Pendentes
--     - Type: Interactive Grid
--     - SQL: SELECT c.compra_id, f.nome fornecedor, c.valor_total, c.data_compra
--            FROM COMPRAS c JOIN FORNECEDORES f ON c.fornecedor_id = f.fornecedor_id
--            WHERE c.status = 'PENDENTE'
--     - Read Only: Yes
--
-- 15. ADICIONE BOTÃO: Atualizar
--     - Name: P1_BTN_REFRESH
--     - Type: Button
--     - Label: ↻ Atualizar
--     - Position: Buttons
--     - Action: Refresh > All
--
-- 16. TESTE A PÁGINA
--     - Clique em "Run Page" ou F10
--     - Verifique se os KPIs aparecem
--     - Verifique se os gráficos renderizam
--     - Teste o botão de atualizar
--
-- =====================================================

-- =====================================================
-- DADOS DE TESTE (Execute se não tiver dados)
-- =====================================================

-- Inserir cliente de teste se não existir
INSERT INTO CLIENTES (nome, cpf, email, telefone, tipo, ativo)
SELECT 'Cliente Teste', '12345678901', 'teste@teste.com', '11987654321', 'FISICO', 'S'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM CLIENTES WHERE cpf = '12345678901');

-- Inserir vendas de teste dos últimos 7 dias
BEGIN
  FOR i IN 0..6 LOOP
    INSERT INTO VENDAS (cliente_id, data_venda, valor_total, valor_final, forma_pagamento, status)
    VALUES (1, TRUNC(SYSDATE) - i, 100 * (i+1), 100 * (i+1), 'DINHEIRO', 'CONCLUIDA');

    -- Inserir itens da venda
    INSERT INTO ITENS_VENDA (venda_id, produto_id, quantidade, preco_unitario, subtotal)
    SELECT MAX(venda_id), 1, i+1, 50, (i+1)*50 FROM VENDAS WHERE cliente_id = 1;
  END LOOP;
  COMMIT;
END;
/

-- Inserir uma compra pendente de teste
INSERT INTO COMPRAS (fornecedor_id, data_compra, valor_total, status)
SELECT 1, SYSDATE, 5000, 'PENDENTE'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM COMPRAS WHERE status = 'PENDENTE' AND fornecedor_id = 1);

COMMIT;

-- =====================================================
-- VERIFICAÇÃO DE DADOS
-- =====================================================

-- Verificar KPIs
SELECT * FROM DASHBOARD_KPIS;

-- Verificar Vendas 7 Dias
SELECT * FROM DASHBOARD_VENDAS_7DIAS;

-- Verificar Top Produtos
SELECT * FROM DASHBOARD_TOP_PRODUTOS WHERE ROWNUM <= 5;

-- Verificar Pagamentos
SELECT * FROM DASHBOARD_PAGAMENTOS;

-- Verificar Produtos em Falta
SELECT produto_id, nome, quantidade, estoque_minimo
FROM PRODUTOS
WHERE quantidade <= estoque_minimo * 1.5
AND ativo = 'S'
ORDER BY quantidade ASC;

-- Verificar Compras Pendentes
SELECT c.compra_id, f.nome, c.valor_total, c.data_compra
FROM COMPRAS c
JOIN FORNECEDORES f ON c.fornecedor_id = f.fornecedor_id
WHERE c.status = 'PENDENTE';

-- =====================================================
-- MENSAGEM DE CONCLUSÃO
-- =====================================================

BEGIN
  DBMS_OUTPUT.PUT_LINE('==================================================');
  DBMS_OUTPUT.PUT_LINE('✓ Views de Dashboard criadas com sucesso!');
  DBMS_OUTPUT.PUT_LINE('✓ Dados de teste inseridos');
  DBMS_OUTPUT.PUT_LINE('');
  DBMS_OUTPUT.PUT_LINE('PRÓXIMO PASSO:');
  DBMS_OUTPUT.PUT_LINE('1. Acesse APEX App Builder');
  DBMS_OUTPUT.PUT_LINE('2. Siga o guia 02_CREATE_HOME_PAGE.md');
  DBMS_OUTPUT.PUT_LINE('3. Crie a página 1 (HOME) manualmente');
  DBMS_OUTPUT.PUT_LINE('');
  DBMS_OUTPUT.PUT_LINE('Você pode usar as queries acima nos componentes!');
  DBMS_OUTPUT.PUT_LINE('==================================================');
END;
/

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================
