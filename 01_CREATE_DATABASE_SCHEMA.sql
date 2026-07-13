-- =====================================================
-- SISTEMA DE GESTÃO DE MERCADO - ORACLE APEX
-- Script de Criação do Schema
-- =====================================================
-- Este script cria todas as tabelas, sequences, views e triggers
-- necessários para o Sistema de Gestão de Mercado

-- =====================================================
-- 1. CRIAR TABELAS
-- =====================================================

-- Tabela de Categorias de Produtos
CREATE TABLE CATEGORIAS (
    categoria_id     NUMBER PRIMARY KEY,
    nome             VARCHAR2(100) NOT NULL,
    descricao        VARCHAR2(500),
    ativa            CHAR(1) DEFAULT 'S' CHECK (ativa IN ('S', 'N')),
    criada_em        TIMESTAMP DEFAULT SYSDATE,
    CONSTRAINT uq_categorias_nome UNIQUE (nome)
);

-- Tabela de Produtos
CREATE TABLE PRODUTOS (
    produto_id       NUMBER PRIMARY KEY,
    categoria_id     NUMBER NOT NULL,
    nome             VARCHAR2(150) NOT NULL,
    descricao        VARCHAR2(500),
    preco_custo      NUMBER(10, 2) NOT NULL,
    preco_venda      NUMBER(10, 2) NOT NULL,
    quantidade       NUMBER(10, 2) DEFAULT 0,
    estoque_minimo   NUMBER(10, 2) DEFAULT 10,
    sku              VARCHAR2(50) NOT NULL,
    ativo            CHAR(1) DEFAULT 'S' CHECK (ativo IN ('S', 'N')),
    criado_em        TIMESTAMP DEFAULT SYSDATE,
    atualizado_em    TIMESTAMP DEFAULT SYSDATE,
    CONSTRAINT fk_produtos_categorias FOREIGN KEY (categoria_id)
        REFERENCES CATEGORIAS(categoria_id),
    CONSTRAINT uq_produtos_sku UNIQUE (sku)
);

-- Tabela de Clientes
CREATE TABLE CLIENTES (
    cliente_id       NUMBER PRIMARY KEY,
    nome             VARCHAR2(150) NOT NULL,
    cpf              VARCHAR2(14),
    email            VARCHAR2(100),
    telefone         VARCHAR2(20),
    endereco         VARCHAR2(300),
    cidade           VARCHAR2(100),
    estado           VARCHAR2(2),
    cep              VARCHAR2(10),
    tipo             VARCHAR2(20) DEFAULT 'FISICO', -- FISICO ou JURIDICO
    ativo            CHAR(1) DEFAULT 'S' CHECK (ativo IN ('S', 'N')),
    criado_em        TIMESTAMP DEFAULT SYSDATE,
    CONSTRAINT uq_clientes_cpf UNIQUE (cpf),
    CONSTRAINT uq_clientes_email UNIQUE (email)
);

-- Tabela de Vendas
CREATE TABLE VENDAS (
    venda_id         NUMBER PRIMARY KEY,
    cliente_id       NUMBER,
    data_venda       DATE DEFAULT SYSDATE NOT NULL,
    valor_total      NUMBER(12, 2) NOT NULL,
    desconto         NUMBER(12, 2) DEFAULT 0,
    valor_final      NUMBER(12, 2) NOT NULL,
    forma_pagamento  VARCHAR2(50) NOT NULL, -- DINHEIRO, CARTAO_CREDITO, CARTAO_DEBITO, PIX, CHEQUE
    status           VARCHAR2(20) DEFAULT 'CONCLUIDA' CHECK (status IN ('PENDENTE', 'CONCLUIDA', 'CANCELADA')),
    observacoes      VARCHAR2(500),
    criada_em        TIMESTAMP DEFAULT SYSDATE,
    CONSTRAINT fk_vendas_clientes FOREIGN KEY (cliente_id)
        REFERENCES CLIENTES(cliente_id)
);

-- Tabela de Itens da Venda
CREATE TABLE ITENS_VENDA (
    item_venda_id    NUMBER PRIMARY KEY,
    venda_id         NUMBER NOT NULL,
    produto_id       NUMBER NOT NULL,
    quantidade       NUMBER(10, 2) NOT NULL,
    preco_unitario   NUMBER(10, 2) NOT NULL,
    desconto_item    NUMBER(12, 2) DEFAULT 0,
    subtotal         NUMBER(12, 2) NOT NULL,
    criado_em        TIMESTAMP DEFAULT SYSDATE,
    CONSTRAINT fk_itens_venda_vendas FOREIGN KEY (venda_id)
        REFERENCES VENDAS(venda_id) ON DELETE CASCADE,
    CONSTRAINT fk_itens_venda_produtos FOREIGN KEY (produto_id)
        REFERENCES PRODUTOS(produto_id)
);

-- Tabela de Movimentação de Estoque
CREATE TABLE MOVIMENTACOES_ESTOQUE (
    movimentacao_id  NUMBER PRIMARY KEY,
    produto_id       NUMBER NOT NULL,
    tipo_movimento   VARCHAR2(20) NOT NULL CHECK (tipo_movimento IN ('ENTRADA', 'SAIDA', 'AJUSTE')),
    quantidade       NUMBER(10, 2) NOT NULL,
    motivo           VARCHAR2(200),
    referencia_id    NUMBER, -- ID da venda ou nota fiscal
    referencia_tipo  VARCHAR2(50), -- VENDA, NOTA_FISCAL, AJUSTE
    criada_em        TIMESTAMP DEFAULT SYSDATE,
    CONSTRAINT fk_movim_estoque_produtos FOREIGN KEY (produto_id)
        REFERENCES PRODUTOS(produto_id)
);

-- Tabela de Fornecedores
CREATE TABLE FORNECEDORES (
    fornecedor_id    NUMBER PRIMARY KEY,
    nome             VARCHAR2(150) NOT NULL,
    cnpj             VARCHAR2(18),
    email            VARCHAR2(100),
    telefone         VARCHAR2(20),
    endereco         VARCHAR2(300),
    cidade           VARCHAR2(100),
    estado           VARCHAR2(2),
    ativo            CHAR(1) DEFAULT 'S' CHECK (ativo IN ('S', 'N')),
    criado_em        TIMESTAMP DEFAULT SYSDATE,
    CONSTRAINT uq_fornecedores_cnpj UNIQUE (cnpj)
);

-- Tabela de Compras
CREATE TABLE COMPRAS (
    compra_id        NUMBER PRIMARY KEY,
    fornecedor_id    NUMBER NOT NULL,
    data_compra      DATE DEFAULT SYSDATE NOT NULL,
    valor_total      NUMBER(12, 2) NOT NULL,
    data_entrega     DATE,
    status           VARCHAR2(20) DEFAULT 'PENDENTE' CHECK (status IN ('PENDENTE', 'RECEBIDA', 'CANCELADA')),
    observacoes      VARCHAR2(500),
    criada_em        TIMESTAMP DEFAULT SYSDATE,
    CONSTRAINT fk_compras_fornecedores FOREIGN KEY (fornecedor_id)
        REFERENCES FORNECEDORES(fornecedor_id)
);

-- Tabela de Itens da Compra
CREATE TABLE ITENS_COMPRA (
    item_compra_id   NUMBER PRIMARY KEY,
    compra_id        NUMBER NOT NULL,
    produto_id       NUMBER NOT NULL,
    quantidade       NUMBER(10, 2) NOT NULL,
    preco_unitario   NUMBER(10, 2) NOT NULL,
    subtotal         NUMBER(12, 2) NOT NULL,
    criado_em        TIMESTAMP DEFAULT SYSDATE,
    CONSTRAINT fk_itens_compra_compras FOREIGN KEY (compra_id)
        REFERENCES COMPRAS(compra_id) ON DELETE CASCADE,
    CONSTRAINT fk_itens_compra_produtos FOREIGN KEY (produto_id)
        REFERENCES PRODUTOS(produto_id)
);

-- =====================================================
-- 2. CRIAR SEQUENCES
-- =====================================================

CREATE SEQUENCE SEQ_CATEGORIAS
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE SEQUENCE SEQ_PRODUTOS
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE SEQUENCE SEQ_CLIENTES
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE SEQUENCE SEQ_VENDAS
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE SEQUENCE SEQ_ITENS_VENDA
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE SEQUENCE SEQ_MOVIM_ESTOQUE
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE SEQUENCE SEQ_FORNECEDORES
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE SEQUENCE SEQ_COMPRAS
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE SEQUENCE SEQ_ITENS_COMPRA
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

-- =====================================================
-- 3. CRIAR TRIGGERS PARA AUTO-INCREMENTO
-- =====================================================

CREATE OR REPLACE TRIGGER TRG_CATEGORIAS_ID
BEFORE INSERT ON CATEGORIAS
FOR EACH ROW
BEGIN
    IF :NEW.categoria_id IS NULL THEN
        SELECT SEQ_CATEGORIAS.NEXTVAL INTO :NEW.categoria_id FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER TRG_PRODUTOS_ID
BEFORE INSERT ON PRODUTOS
FOR EACH ROW
BEGIN
    IF :NEW.produto_id IS NULL THEN
        SELECT SEQ_PRODUTOS.NEXTVAL INTO :NEW.produto_id FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER TRG_CLIENTES_ID
BEFORE INSERT ON CLIENTES
FOR EACH ROW
BEGIN
    IF :NEW.cliente_id IS NULL THEN
        SELECT SEQ_CLIENTES.NEXTVAL INTO :NEW.cliente_id FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER TRG_VENDAS_ID
BEFORE INSERT ON VENDAS
FOR EACH ROW
BEGIN
    IF :NEW.venda_id IS NULL THEN
        SELECT SEQ_VENDAS.NEXTVAL INTO :NEW.venda_id FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER TRG_ITENS_VENDA_ID
BEFORE INSERT ON ITENS_VENDA
FOR EACH ROW
BEGIN
    IF :NEW.item_venda_id IS NULL THEN
        SELECT SEQ_ITENS_VENDA.NEXTVAL INTO :NEW.item_venda_id FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER TRG_MOVIM_ESTOQUE_ID
BEFORE INSERT ON MOVIMENTACOES_ESTOQUE
FOR EACH ROW
BEGIN
    IF :NEW.movimentacao_id IS NULL THEN
        SELECT SEQ_MOVIM_ESTOQUE.NEXTVAL INTO :NEW.movimentacao_id FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER TRG_FORNECEDORES_ID
BEFORE INSERT ON FORNECEDORES
FOR EACH ROW
BEGIN
    IF :NEW.fornecedor_id IS NULL THEN
        SELECT SEQ_FORNECEDORES.NEXTVAL INTO :NEW.fornecedor_id FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER TRG_COMPRAS_ID
BEFORE INSERT ON COMPRAS
FOR EACH ROW
BEGIN
    IF :NEW.compra_id IS NULL THEN
        SELECT SEQ_COMPRAS.NEXTVAL INTO :NEW.compra_id FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER TRG_ITENS_COMPRA_ID
BEFORE INSERT ON ITENS_COMPRA
FOR EACH ROW
BEGIN
    IF :NEW.item_compra_id IS NULL THEN
        SELECT SEQ_ITENS_COMPRA.NEXTVAL INTO :NEW.item_compra_id FROM DUAL;
    END IF;
END;
/

-- =====================================================
-- 4. CRIAR TRIGGERS PARA ATUALIZAR ESTOQUE
-- =====================================================

-- Trigger para atualizar estoque quando venda é concluída
CREATE OR REPLACE TRIGGER TRG_VENDA_ATUALIZA_ESTOQUE
AFTER INSERT ON ITENS_VENDA
FOR EACH ROW
BEGIN
    -- Reduz estoque
    UPDATE PRODUTOS
    SET quantidade = quantidade - :NEW.quantidade
    WHERE produto_id = :NEW.produto_id;

    -- Registra movimentação
    INSERT INTO MOVIMENTACOES_ESTOQUE (
        movimentacao_id, produto_id, tipo_movimento, quantidade,
        motivo, referencia_id, referencia_tipo
    ) VALUES (
        NULL, :NEW.produto_id, 'SAIDA', :NEW.quantidade,
        'Venda #' || :NEW.venda_id, :NEW.venda_id, 'VENDA'
    );
END;
/

-- Trigger para atualizar estoque quando compra é recebida
CREATE OR REPLACE TRIGGER TRG_COMPRA_ATUALIZA_ESTOQUE
AFTER INSERT ON ITENS_COMPRA
FOR EACH ROW
BEGIN
    -- Aumenta estoque
    UPDATE PRODUTOS
    SET quantidade = quantidade + :NEW.quantidade
    WHERE produto_id = :NEW.produto_id;

    -- Registra movimentação
    INSERT INTO MOVIMENTACOES_ESTOQUE (
        movimentacao_id, produto_id, tipo_movimento, quantidade,
        motivo, referencia_id, referencia_tipo
    ) VALUES (
        NULL, :NEW.produto_id, 'ENTRADA', :NEW.quantidade,
        'Compra #' || :NEW.compra_id, :NEW.compra_id, 'COMPRA'
    );
END;
/

-- =====================================================
-- 5. CRIAR VIEWS
-- =====================================================

-- View: Produtos com Alerta de Estoque Baixo
CREATE OR REPLACE VIEW PRODUTOS_COM_ALERTA AS
SELECT
    p.produto_id,
    p.nome,
    c.nome AS categoria,
    p.quantidade,
    p.estoque_minimo,
    CASE
        WHEN p.quantidade <= p.estoque_minimo THEN 'CRÍTICO'
        WHEN p.quantidade <= (p.estoque_minimo * 1.5) THEN 'BAIXO'
        ELSE 'NORMAL'
    END AS status_estoque,
    p.preco_venda
FROM PRODUTOS p
INNER JOIN CATEGORIAS c ON p.categoria_id = c.categoria_id
WHERE p.ativo = 'S'
ORDER BY p.quantidade ASC;

-- View: Dashboard de Vendas Diárias
CREATE OR REPLACE VIEW VENDAS_DIARIAS AS
SELECT
    TRUNC(v.data_venda) AS data,
    COUNT(v.venda_id) AS qtd_vendas,
    SUM(v.valor_final) AS total_vendido,
    AVG(v.valor_final) AS ticket_medio
FROM VENDAS v
WHERE v.status = 'CONCLUIDA'
GROUP BY TRUNC(v.data_venda)
ORDER BY TRUNC(v.data_venda) DESC;

-- View: Produtos Mais Vendidos
CREATE OR REPLACE VIEW PRODUTOS_MAIS_VENDIDOS AS
SELECT
    p.produto_id,
    p.nome,
    c.nome AS categoria,
    SUM(iv.quantidade) AS quantidade_vendida,
    SUM(iv.subtotal) AS valor_total_vendido,
    COUNT(DISTINCT iv.venda_id) AS qtd_transacoes
FROM ITENS_VENDA iv
INNER JOIN PRODUTOS p ON iv.produto_id = p.produto_id
INNER JOIN CATEGORIAS c ON p.categoria_id = c.categoria_id
GROUP BY p.produto_id, p.nome, c.nome
ORDER BY quantidade_vendida DESC;

-- View: Saldo de Clientes (Crediário)
CREATE OR REPLACE VIEW SALDO_CLIENTES AS
SELECT
    c.cliente_id,
    c.nome,
    COUNT(v.venda_id) AS qtd_compras,
    SUM(v.valor_final) AS total_gasto,
    MAX(v.data_venda) AS ultima_compra
FROM CLIENTES c
LEFT JOIN VENDAS v ON c.cliente_id = v.cliente_id AND v.status = 'CONCLUIDA'
WHERE c.ativo = 'S'
GROUP BY c.cliente_id, c.nome
ORDER BY total_gasto DESC;

-- =====================================================
-- 6. CRIAR PROCEDURES
-- =====================================================

-- Procedure para Finalizar Venda (Exemplo)
CREATE OR REPLACE PROCEDURE FINALIZAR_VENDA (
    p_venda_id IN NUMBER,
    p_status OUT VARCHAR2
) AS
    v_venda_existe NUMBER;
    v_total NUMBER(12, 2);
BEGIN
    -- Verifica se a venda existe
    SELECT COUNT(*) INTO v_venda_existe
    FROM VENDAS
    WHERE venda_id = p_venda_id;

    IF v_venda_existe = 0 THEN
        p_status := 'ERRO: Venda não encontrada';
        RETURN;
    END IF;

    -- Calcula o total com base nos itens
    SELECT SUM(subtotal) INTO v_total
    FROM ITENS_VENDA
    WHERE venda_id = p_venda_id;

    -- Atualiza a venda
    UPDATE VENDAS
    SET status = 'CONCLUIDA',
        valor_final = v_total
    WHERE venda_id = p_venda_id;

    p_status := 'OK: Venda finalizada com sucesso';
    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        p_status := 'ERRO: ' || SQLERRM;
        ROLLBACK;
END FINALIZAR_VENDA;
/

-- =====================================================
-- 7. INSERIR DADOS DE EXEMPLO
-- =====================================================

-- Inserir Categorias
INSERT INTO CATEGORIAS (nome, descricao) VALUES ('Alimentos', 'Produtos alimentares variados');
INSERT INTO CATEGORIAS (nome, descricao) VALUES ('Bebidas', 'Bebidas em geral');
INSERT INTO CATEGORIAS (nome, descricao) VALUES ('Higiene e Limpeza', 'Produtos de higiene e limpeza');
INSERT INTO CATEGORIAS (nome, descricao) VALUES ('Eletrônicos', 'Produtos eletrônicos');
INSERT INTO CATEGORIAS (nome, descricao) VALUES ('Vestuário', 'Roupas e acessórios');

COMMIT;

-- Inserir Produtos de Exemplo
INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (1, 'Arroz Integral 5kg', 'Arroz integral de alta qualidade', 15.00, 24.90, 50, 10, 'ARR-INT-5K', 'S');

INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (1, 'Feijão Carioca 1kg', 'Feijão carioca premium', 4.50, 7.90, 80, 20, 'FEI-CAR-1K', 'S');

INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (2, 'Suco Natural 1L', 'Suco natural laranja', 3.20, 5.90, 100, 30, 'SUC-LAR-1L', 'S');

INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (2, 'Água Mineral 1.5L', 'Água mineral sem gás', 1.50, 2.99, 200, 50, 'AGU-MIN-1.5', 'S');

INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (3, 'Detergente Neutro 500ml', 'Detergente neutro eficaz', 2.00, 3.50, 120, 25, 'DET-NEU-500', 'S');

INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (3, 'Sabonete Líquido 250ml', 'Sabonete líquido para mãos', 3.50, 6.90, 150, 40, 'SAB-LIQ-250', 'S');

INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (4, 'Fone de Ouvido Bluetooth', 'Fone de ouvido com Bluetooth', 35.00, 79.90, 25, 5, 'FON-BLU-001', 'S');

INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (4, 'Carregador USB Tipo C', 'Carregador rápido USB-C', 12.00, 29.90, 60, 15, 'CAR-USB-C', 'S');

INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (5, 'Camiseta Básica Preta', 'Camiseta de algodão 100%', 15.00, 39.90, 100, 20, 'CAM-PRT-M', 'S');

INSERT INTO PRODUTOS (categoria_id, nome, descricao, preco_custo, preco_venda, quantidade, estoque_minimo, sku, ativo)
VALUES (5, 'Calça Jeans Azul', 'Calça jeans premium', 40.00, 99.90, 50, 10, 'CAL-JEN-M', 'S');

COMMIT;

-- Inserir Clientes de Exemplo
INSERT INTO CLIENTES (nome, cpf, email, telefone, endereco, cidade, estado, tipo, ativo)
VALUES ('João Silva', '12345678901', 'joao@email.com', '11987654321', 'Rua A, 123', 'São Paulo', 'SP', 'FISICO', 'S');

INSERT INTO CLIENTES (nome, cpf, email, telefone, endereco, cidade, estado, tipo, ativo)
VALUES ('Maria Santos', '98765432101', 'maria@email.com', '11912345678', 'Rua B, 456', 'São Paulo', 'SP', 'FISICO', 'S');

INSERT INTO CLIENTES (nome, cpf, email, telefone, endereco, cidade, estado, tipo, ativo)
VALUES ('Empresa XYZ', '12345678000190', 'contato@xyz.com', '1133334444', 'Avenida C, 789', 'São Paulo', 'SP', 'JURIDICO', 'S');

COMMIT;

-- Inserir Fornecedores de Exemplo
INSERT INTO FORNECEDORES (nome, cnpj, email, telefone, endereco, cidade, estado, ativo)
VALUES ('Distribuidora ABC', '12345678000100', 'abc@abc.com', '1133331111', 'Rua D, 111', 'Guarulhos', 'SP', 'S');

INSERT INTO FORNECEDORES (nome, cnpj, email, telefone, endereco, cidade, estado, ativo)
VALUES ('Supplier XYZ', '98765432000150', 'xyz@supplier.com', '1144442222', 'Rua E, 222', 'Osasco', 'SP', 'S');

COMMIT;

-- =====================================================
-- 8. MENSAGEM DE SUCESSO
-- =====================================================

BEGIN
    DBMS_OUTPUT.PUT_LINE('==================================================');
    DBMS_OUTPUT.PUT_LINE('Sistema de Gestão de Mercado');
    DBMS_OUTPUT.PUT_LINE('Base de dados criada com sucesso!');
    DBMS_OUTPUT.PUT_LINE('==================================================');
    DBMS_OUTPUT.PUT_LINE(' ');
    DBMS_OUTPUT.PUT_LINE('✓ Tabelas criadas: 8');
    DBMS_OUTPUT.PUT_LINE('✓ Sequences criadas: 9');
    DBMS_OUTPUT.PUT_LINE('✓ Triggers criados: 10');
    DBMS_OUTPUT.PUT_LINE('✓ Views criadas: 5');
    DBMS_OUTPUT.PUT_LINE('✓ Procedures criadas: 1');
    DBMS_OUTPUT.PUT_LINE('✓ Dados de exemplo: 10 produtos, 3 clientes, 2 fornecedores');
    DBMS_OUTPUT.PUT_LINE(' ');
    DBMS_OUTPUT.PUT_LINE('Próximo passo: Criar o Workspace APEX');
    DBMS_OUTPUT.PUT_LINE('==================================================');
END;
/

COMMIT;
