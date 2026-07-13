-- =====================================================
-- VIEWS E PROCEDURES COMPLETAS
-- Sistema de Gestão de Mercado - APEX
-- =====================================================
-- Este script cria TODAS as views e procedures
-- necessárias para o sistema completo
-- =====================================================

-- =====================================================
-- VIEWS JÁ CRIADAS (Referência)
-- =====================================================
-- ✓ PRODUTOS_COM_ALERTA
-- ✓ VENDAS_DIARIAS
-- ✓ PRODUTOS_MAIS_VENDIDOS
-- ✓ SALDO_CLIENTES
-- ✓ DASHBOARD_KPIS
-- ✓ DASHBOARD_VENDAS_7DIAS
-- ✓ DASHBOARD_TOP_PRODUTOS
-- ✓ DASHBOARD_PAGAMENTOS

-- =====================================================
-- NOVAS VIEWS PARA COMPLEMENTAR
-- =====================================================

-- View: Lista Completa de Produtos com Categoria
CREATE OR REPLACE VIEW V_PRODUTOS_COMPLETO AS
SELECT
  p.produto_id,
  p.nome,
  p.descricao,
  p.sku,
  c.categoria_id,
  c.nome as categoria,
  p.preco_custo,
  p.preco_venda,
  p.quantidade,
  p.estoque_minimo,
  ROUND(((p.preco_venda - p.preco_custo) / p.preco_custo * 100), 2) as margem_percentual,
  p.ativo,
  p.criado_em,
  p.atualizado_em
FROM PRODUTOS p
LEFT JOIN CATEGORIAS c ON p.categoria_id = c.categoria_id
ORDER BY p.nome;

-- View: Histórico de Vendas Detalhado
CREATE OR REPLACE VIEW V_VENDAS_DETALHADO AS
SELECT
  v.venda_id,
  v.data_venda,
  c.cliente_id,
  c.nome as cliente,
  c.cpf,
  c.email,
  v.valor_total,
  v.desconto,
  v.valor_final,
  v.forma_pagamento,
  v.status,
  COUNT(iv.item_venda_id) as qtd_itens,
  v.criada_em
FROM VENDAS v
LEFT JOIN CLIENTES c ON v.cliente_id = c.cliente_id
LEFT JOIN ITENS_VENDA iv ON v.venda_id = iv.venda_id
GROUP BY
  v.venda_id, v.data_venda, c.cliente_id, c.nome, c.cpf, c.email,
  v.valor_total, v.desconto, v.valor_final, v.forma_pagamento, v.status, v.criada_em
ORDER BY v.data_venda DESC;

-- View: Itens de Venda com Detalhes
CREATE OR REPLACE VIEW V_ITENS_VENDA_DETALHADO AS
SELECT
  iv.item_venda_id,
  iv.venda_id,
  iv.produto_id,
  p.nome as produto,
  p.sku,
  iv.quantidade,
  iv.preco_unitario,
  iv.desconto_item,
  iv.subtotal,
  (iv.preco_unitario - p.preco_custo) * iv.quantidade as lucro_bruto
FROM ITENS_VENDA iv
JOIN PRODUTOS p ON iv.produto_id = p.produto_id
ORDER BY iv.venda_id DESC;

-- View: Clientes com Último Movimento
CREATE OR REPLACE VIEW V_CLIENTES_COMPLETO AS
SELECT
  c.cliente_id,
  c.nome,
  c.cpf,
  c.email,
  c.telefone,
  c.endereco,
  c.cidade,
  c.estado,
  c.cep,
  c.tipo,
  c.ativo,
  COUNT(DISTINCT v.venda_id) as qtd_compras,
  NVL(SUM(v.valor_final), 0) as total_gasto,
  MAX(v.data_venda) as ultima_compra
FROM CLIENTES c
LEFT JOIN VENDAS v ON c.cliente_id = v.cliente_id AND v.status = 'CONCLUIDA'
GROUP BY
  c.cliente_id, c.nome, c.cpf, c.email, c.telefone, c.endereco,
  c.cidade, c.estado, c.cep, c.tipo, c.ativo
ORDER BY c.nome;

-- View: Compras com Detalhes
CREATE OR REPLACE VIEW V_COMPRAS_DETALHADO AS
SELECT
  c.compra_id,
  c.data_compra,
  f.fornecedor_id,
  f.nome as fornecedor,
  f.cnpj,
  f.email,
  c.valor_total,
  c.data_entrega,
  c.status,
  COUNT(ic.item_compra_id) as qtd_itens,
  c.criada_em
FROM COMPRAS c
LEFT JOIN FORNECEDORES f ON c.fornecedor_id = f.fornecedor_id
LEFT JOIN ITENS_COMPRA ic ON c.compra_id = ic.compra_id
GROUP BY
  c.compra_id, c.data_compra, f.fornecedor_id, f.nome, f.cnpj, f.email,
  c.valor_total, c.data_entrega, c.status, c.criada_em
ORDER BY c.data_compra DESC;

-- View: Itens de Compra com Detalhes
CREATE OR REPLACE VIEW V_ITENS_COMPRA_DETALHADO AS
SELECT
  ic.item_compra_id,
  ic.compra_id,
  ic.produto_id,
  p.nome as produto,
  p.sku,
  ic.quantidade,
  ic.preco_unitario,
  ic.subtotal
FROM ITENS_COMPRA ic
JOIN PRODUTOS p ON ic.produto_id = p.produto_id
ORDER BY ic.compra_id DESC;

-- View: Movimentações com Detalhes
CREATE OR REPLACE VIEW V_MOVIMENTACOES_DETALHADO AS
SELECT
  m.movimentacao_id,
  m.produto_id,
  p.nome as produto,
  m.tipo_movimento,
  m.quantidade,
  m.motivo,
  m.referencia_id,
  m.referencia_tipo,
  m.criada_em
FROM MOVIMENTACOES_ESTOQUE m
LEFT JOIN PRODUTOS p ON m.produto_id = p.produto_id
ORDER BY m.criada_em DESC;

-- View: Estoque Atual com Status
CREATE OR REPLACE VIEW V_ESTOQUE_STATUS AS
SELECT
  p.produto_id,
  p.nome,
  c.nome as categoria,
  p.sku,
  p.quantidade,
  p.estoque_minimo,
  p.quantidade - p.estoque_minimo as diferenca,
  CASE
    WHEN p.quantidade <= p.estoque_minimo THEN 'CRÍTICO'
    WHEN p.quantidade <= (p.estoque_minimo * 1.5) THEN 'BAIXO'
    WHEN p.quantidade > (p.estoque_minimo * 3) THEN 'ALTO'
    ELSE 'NORMAL'
  END as status_estoque,
  CASE
    WHEN p.quantidade <= p.estoque_minimo THEN 1
    WHEN p.quantidade <= (p.estoque_minimo * 1.5) THEN 2
    WHEN p.quantidade > (p.estoque_minimo * 3) THEN 3
    ELSE 2
  END as prioridade
FROM PRODUTOS p
LEFT JOIN CATEGORIAS c ON p.categoria_id = c.categoria_id
WHERE p.ativo = 'S'
ORDER BY prioridade, p.quantidade ASC;

-- View: Análise de Vendas por Período
CREATE OR REPLACE VIEW V_VENDAS_PERIODO AS
SELECT
  TRUNC(v.data_venda) as data,
  TO_CHAR(v.data_venda, 'DD/MM/YYYY') as data_fmt,
  TO_CHAR(v.data_venda, 'Day') as dia_semana,
  COUNT(DISTINCT v.venda_id) as qtd_vendas,
  COUNT(DISTINCT v.cliente_id) as qtd_clientes,
  SUM(v.valor_final) as total_vendido,
  AVG(v.valor_final) as ticket_medio,
  SUM(v.desconto) as desconto_total
FROM VENDAS v
WHERE v.status = 'CONCLUIDA'
GROUP BY TRUNC(v.data_venda), TO_CHAR(v.data_venda, 'DD/MM/YYYY'), TO_CHAR(v.data_venda, 'Day')
ORDER BY TRUNC(v.data_venda) DESC;

-- View: Relatório de Lucro por Produto
CREATE OR REPLACE VIEW V_LUCRO_PRODUTO AS
SELECT
  p.produto_id,
  p.nome,
  c.nome as categoria,
  SUM(iv.quantidade) as quantidade_vendida,
  SUM(iv.subtotal) as faturamento,
  SUM((iv.preco_unitario - p.preco_custo) * iv.quantidade) as lucro_bruto,
  ROUND(SUM((iv.preco_unitario - p.preco_custo) * iv.quantidade) / SUM(iv.subtotal) * 100, 2) as margem_percentual
FROM ITENS_VENDA iv
JOIN PRODUTOS p ON iv.produto_id = p.produto_id
LEFT JOIN CATEGORIAS c ON p.categoria_id = c.categoria_id
JOIN VENDAS v ON iv.venda_id = v.venda_id AND v.status = 'CONCLUIDA'
GROUP BY p.produto_id, p.nome, c.nome
ORDER BY lucro_bruto DESC;

-- View: Fornecedores com Histórico
CREATE OR REPLACE VIEW V_FORNECEDORES_COMPLETO AS
SELECT
  f.fornecedor_id,
  f.nome,
  f.cnpj,
  f.email,
  f.telefone,
  f.endereco,
  f.cidade,
  f.estado,
  f.ativo,
  COUNT(DISTINCT c.compra_id) as qtd_compras,
  NVL(SUM(c.valor_total), 0) as total_comprado,
  MAX(c.data_compra) as ultima_compra
FROM FORNECEDORES f
LEFT JOIN COMPRAS c ON f.fornecedor_id = c.fornecedor_id
GROUP BY
  f.fornecedor_id, f.nome, f.cnpj, f.email, f.telefone,
  f.endereco, f.cidade, f.estado, f.ativo
ORDER BY f.nome;

-- =====================================================
-- PROCEDURES NOVAS
-- =====================================================

-- Procedure: Criar Venda Completa
CREATE OR REPLACE PROCEDURE SP_CRIAR_VENDA (
  p_cliente_id IN NUMBER,
  p_forma_pagamento IN VARCHAR2,
  p_desconto IN NUMBER DEFAULT 0,
  p_venda_id OUT NUMBER,
  p_status OUT VARCHAR2
) AS
  v_total NUMBER(12, 2) := 0;
BEGIN
  -- Criar venda
  INSERT INTO VENDAS (
    cliente_id, data_venda, valor_total, desconto, valor_final,
    forma_pagamento, status
  ) VALUES (
    p_cliente_id, SYSDATE, 0, p_desconto, 0,
    p_forma_pagamento, 'PENDENTE'
  ) RETURNING venda_id INTO p_venda_id;

  p_status := 'OK: Venda #' || p_venda_id || ' criada com sucesso';
  COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    p_status := 'ERRO: ' || SQLERRM;
    ROLLBACK;
END SP_CRIAR_VENDA;
/

-- Procedure: Adicionar Item à Venda
CREATE OR REPLACE PROCEDURE SP_ADICIONAR_ITEM_VENDA (
  p_venda_id IN NUMBER,
  p_produto_id IN NUMBER,
  p_quantidade IN NUMBER,
  p_desconto_item IN NUMBER DEFAULT 0,
  p_status OUT VARCHAR2
) AS
  v_preco_venda NUMBER(10, 2);
  v_subtotal NUMBER(12, 2);
BEGIN
  -- Buscar preço
  SELECT preco_venda INTO v_preco_venda
  FROM PRODUTOS WHERE produto_id = p_produto_id;

  -- Calcular subtotal
  v_subtotal := (v_preco_venda * p_quantidade) - p_desconto_item;

  -- Inserir item
  INSERT INTO ITENS_VENDA (
    venda_id, produto_id, quantidade, preco_unitario, desconto_item, subtotal
  ) VALUES (
    p_venda_id, p_produto_id, p_quantidade, v_preco_venda, p_desconto_item, v_subtotal
  );

  -- Atualizar total da venda
  UPDATE VENDAS
  SET valor_total = (SELECT SUM(subtotal) FROM ITENS_VENDA WHERE venda_id = p_venda_id),
      valor_final = (SELECT SUM(subtotal) FROM ITENS_VENDA WHERE venda_id = p_venda_id) - NVL(desconto, 0)
  WHERE venda_id = p_venda_id;

  p_status := 'OK: Item adicionado com sucesso';
  COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    p_status := 'ERRO: ' || SQLERRM;
    ROLLBACK;
END SP_ADICIONAR_ITEM_VENDA;
/

-- Procedure: Finalizar Venda
CREATE OR REPLACE PROCEDURE SP_FINALIZAR_VENDA (
  p_venda_id IN NUMBER,
  p_status OUT VARCHAR2
) AS
  v_qtd_itens NUMBER;
  v_valor_final NUMBER(12, 2);
BEGIN
  -- Verificar se tem itens
  SELECT COUNT(*) INTO v_qtd_itens FROM ITENS_VENDA WHERE venda_id = p_venda_id;

  IF v_qtd_itens = 0 THEN
    p_status := 'ERRO: Venda sem itens';
    RETURN;
  END IF;

  -- Buscar valor final
  SELECT valor_final INTO v_valor_final FROM VENDAS WHERE venda_id = p_venda_id;

  -- Atualizar status
  UPDATE VENDAS SET status = 'CONCLUIDA' WHERE venda_id = p_venda_id;

  p_status := 'OK: Venda finalizada com valor ' || v_valor_final;
  COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    p_status := 'ERRO: ' || SQLERRM;
    ROLLBACK;
END SP_FINALIZAR_VENDA;
/

-- Procedure: Cancelar Venda
CREATE OR REPLACE PROCEDURE SP_CANCELAR_VENDA (
  p_venda_id IN NUMBER,
  p_motivo IN VARCHAR2 DEFAULT 'Cancelamento geral',
  p_status OUT VARCHAR2
) AS
BEGIN
  UPDATE VENDAS SET status = 'CANCELADA' WHERE venda_id = p_venda_id;

  -- Registrar movimentação reversa para cada item
  INSERT INTO MOVIMENTACOES_ESTOQUE (produto_id, tipo_movimento, quantidade, motivo, referencia_id, referencia_tipo)
  SELECT produto_id, 'ENTRADA', quantidade, p_motivo || ' - Venda #' || p_venda_id, p_venda_id, 'DEVOLUCAO'
  FROM ITENS_VENDA WHERE venda_id = p_venda_id;

  -- Atualizar estoque
  UPDATE PRODUTOS p
  SET quantidade = quantidade + (SELECT SUM(quantidade) FROM ITENS_VENDA WHERE venda_id = p_venda_id AND produto_id = p.produto_id)
  WHERE produto_id IN (SELECT produto_id FROM ITENS_VENDA WHERE venda_id = p_venda_id);

  p_status := 'OK: Venda cancelada com sucesso';
  COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    p_status := 'ERRO: ' || SQLERRM;
    ROLLBACK;
END SP_CANCELAR_VENDA;
/

-- Procedure: Criar Pedido de Compra
CREATE OR REPLACE PROCEDURE SP_CRIAR_COMPRA (
  p_fornecedor_id IN NUMBER,
  p_data_entrega IN DATE DEFAULT NULL,
  p_compra_id OUT NUMBER,
  p_status OUT VARCHAR2
) AS
BEGIN
  INSERT INTO COMPRAS (
    fornecedor_id, data_compra, valor_total, data_entrega, status
  ) VALUES (
    p_fornecedor_id, SYSDATE, 0, NVL(p_data_entrega, SYSDATE + 7), 'PENDENTE'
  ) RETURNING compra_id INTO p_compra_id;

  p_status := 'OK: Compra #' || p_compra_id || ' criada';
  COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    p_status := 'ERRO: ' || SQLERRM;
    ROLLBACK;
END SP_CRIAR_COMPRA;
/

-- Procedure: Receber Compra
CREATE OR REPLACE PROCEDURE SP_RECEBER_COMPRA (
  p_compra_id IN NUMBER,
  p_status OUT VARCHAR2
) AS
  v_qtd_itens NUMBER;
BEGIN
  -- Verificar itens
  SELECT COUNT(*) INTO v_qtd_itens FROM ITENS_COMPRA WHERE compra_id = p_compra_id;

  IF v_qtd_itens = 0 THEN
    p_status := 'ERRO: Compra sem itens';
    RETURN;
  END IF;

  -- Atualizar status da compra
  UPDATE COMPRAS SET status = 'RECEBIDA', data_entrega = SYSDATE WHERE compra_id = p_compra_id;

  p_status := 'OK: Compra recebida com sucesso';
  COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    p_status := 'ERRO: ' || SQLERRM;
    ROLLBACK;
END SP_RECEBER_COMPRA;
/

-- Procedure: Ajustar Estoque Manual
CREATE OR REPLACE PROCEDURE SP_AJUSTAR_ESTOQUE (
  p_produto_id IN NUMBER,
  p_quantidade IN NUMBER,
  p_motivo IN VARCHAR2,
  p_status OUT VARCHAR2
) AS
BEGIN
  -- Atualizar quantidade
  UPDATE PRODUTOS SET quantidade = quantidade + p_quantidade WHERE produto_id = p_produto_id;

  -- Registrar movimentação
  INSERT INTO MOVIMENTACOES_ESTOQUE (
    produto_id, tipo_movimento, quantidade, motivo, referencia_tipo
  ) VALUES (
    p_produto_id, CASE WHEN p_quantidade > 0 THEN 'ENTRADA' ELSE 'SAIDA' END,
    ABS(p_quantidade), p_motivo, 'AJUSTE'
  );

  p_status := 'OK: Estoque ajustado com sucesso';
  COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    p_status := 'ERRO: ' || SQLERRM;
    ROLLBACK;
END SP_AJUSTAR_ESTOQUE;
/

-- =====================================================
-- VERIFICAÇÃO FINAL
-- =====================================================

BEGIN
  DBMS_OUTPUT.PUT_LINE('==================================================');
  DBMS_OUTPUT.PUT_LINE('✓ Views criadas: 11');
  DBMS_OUTPUT.PUT_LINE('✓ Procedures criadas: 6');
  DBMS_OUTPUT.PUT_LINE('✓ Total de objetos: 17');
  DBMS_OUTPUT.PUT_LINE('');
  DBMS_OUTPUT.PUT_LINE('Views criadas:');
  DBMS_OUTPUT.PUT_LINE('  1. V_PRODUTOS_COMPLETO');
  DBMS_OUTPUT.PUT_LINE('  2. V_VENDAS_DETALHADO');
  DBMS_OUTPUT.PUT_LINE('  3. V_ITENS_VENDA_DETALHADO');
  DBMS_OUTPUT.PUT_LINE('  4. V_CLIENTES_COMPLETO');
  DBMS_OUTPUT.PUT_LINE('  5. V_COMPRAS_DETALHADO');
  DBMS_OUTPUT.PUT_LINE('  6. V_ITENS_COMPRA_DETALHADO');
  DBMS_OUTPUT.PUT_LINE('  7. V_MOVIMENTACOES_DETALHADO');
  DBMS_OUTPUT.PUT_LINE('  8. V_ESTOQUE_STATUS');
  DBMS_OUTPUT.PUT_LINE('  9. V_VENDAS_PERIODO');
  DBMS_OUTPUT.PUT_LINE(' 10. V_LUCRO_PRODUTO');
  DBMS_OUTPUT.PUT_LINE(' 11. V_FORNECEDORES_COMPLETO');
  DBMS_OUTPUT.PUT_LINE('');
  DBMS_OUTPUT.PUT_LINE('Procedures criadas:');
  DBMS_OUTPUT.PUT_LINE('  1. SP_CRIAR_VENDA');
  DBMS_OUTPUT.PUT_LINE('  2. SP_ADICIONAR_ITEM_VENDA');
  DBMS_OUTPUT.PUT_LINE('  3. SP_FINALIZAR_VENDA');
  DBMS_OUTPUT.PUT_LINE('  4. SP_CANCELAR_VENDA');
  DBMS_OUTPUT.PUT_LINE('  5. SP_CRIAR_COMPRA');
  DBMS_OUTPUT.PUT_LINE('  6. SP_RECEBER_COMPRA');
  DBMS_OUTPUT.PUT_LINE('  7. SP_AJUSTAR_ESTOQUE');
  DBMS_OUTPUT.PUT_LINE('');
  DBMS_OUTPUT.PUT_LINE('Sistema pronto para APEX! ✅');
  DBMS_OUTPUT.PUT_LINE('==================================================');
END;
/

COMMIT;
