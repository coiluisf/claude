# ⚡ Guia Rápido: Criar Página HOME em 15 minutos

**Para quem quer criar a página HOME rápido e eficiente.**

---

## 🚀 3 Opções (Escolha Uma)

### Opção A: Manual (Recomendado - 20 min)
Vá para: `02_CREATE_HOME_PAGE.md`
- Mais didático
- Você entende cada passo
- Melhor para primeira vez

### Opção B: Semi-Automático (15 min)
Siga este guia agora ⬇️

### Opção C: Automático (Se souber APEX - 10 min)
Use ferramentas de exportação/importação APEX

---

## ⚡ Começo Rápido (Opção B)

### PASSO 1: Preparar Dados no SQL (2 min)

1. Abra: **SQL Developer Web**
2. Cole este código:

```sql
-- Views para o Dashboard
CREATE OR REPLACE VIEW DASHBOARD_KPIS AS
SELECT
  NVL(SUM(CASE WHEN TRUNC(v.data_venda) = TRUNC(SYSDATE) AND v.status = 'CONCLUIDA' THEN v.valor_final ELSE 0 END), 0) as vendas_hoje,
  NVL(SUM(CASE WHEN TRUNC(v.data_venda, 'MM') = TRUNC(SYSDATE, 'MM') AND v.status = 'CONCLUIDA' THEN v.valor_final ELSE 0 END), 0) as faturamento_mes,
  (SELECT COUNT(*) FROM PRODUTOS WHERE quantidade <= estoque_minimo AND ativo = 'S') as produtos_falta,
  (SELECT COUNT(*) FROM CLIENTES WHERE ativo = 'S') as clientes_ativos,
  SYSDATE as data_referencia
FROM VENDAS v
GROUP BY SYSDATE;

CREATE OR REPLACE VIEW DASHBOARD_VENDAS_7DIAS AS
SELECT
  TRUNC(data_venda) as data,
  TO_CHAR(data_venda, 'DD/MM') as data_fmt,
  SUM(valor_final) as total_vendido
FROM VENDAS
WHERE data_venda >= TRUNC(SYSDATE) - 7 AND status = 'CONCLUIDA'
GROUP BY TRUNC(data_venda), TO_CHAR(data_venda, 'DD/MM')
ORDER BY data DESC;

CREATE OR REPLACE VIEW DASHBOARD_TOP_PRODUTOS AS
SELECT nome, SUM(iv.quantidade) as qtd
FROM ITENS_VENDA iv
JOIN PRODUTOS p ON iv.produto_id = p.produto_id
WHERE iv.criado_em >= TRUNC(SYSDATE) - 30
GROUP BY p.nome
ORDER BY qtd DESC;

CREATE OR REPLACE VIEW DASHBOARD_PAGAMENTOS AS
SELECT forma_pagamento, COUNT(*) as qtd
FROM VENDAS
WHERE status = 'CONCLUIDA' AND data_venda >= TRUNC(SYSDATE) - 30
GROUP BY forma_pagamento;

-- Dados de teste
INSERT INTO CLIENTES (nome, cpf, email, telefone, tipo)
SELECT 'Teste', '12345678901', 'teste@test.com', '11987654321', 'FISICO' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM CLIENTES WHERE cpf = '12345678901');

BEGIN
  FOR i IN 0..6 LOOP
    INSERT INTO VENDAS (cliente_id, data_venda, valor_total, valor_final, forma_pagamento, status)
    VALUES (1, TRUNC(SYSDATE)-i, 100+i*10, 100+i*10, 'DINHEIRO', 'CONCLUIDA');
  END LOOP;
  COMMIT;
END;
/

COMMIT;
```

3. Clique **Run** (Ctrl+Enter)
4. Pronto! ✅

---

### PASSO 2: Criar Página no APEX (10 min)

1. Acesse seu **App Builder APEX**
2. Clique em sua app **"Sistema de Gestão de Mercado"**

#### 2.1 Criar Página Base
```
Clique: + (Create)
Selecione: Blank Page
Page Number: 1
Page Name: HOME
Page Title: Home
Clique: Create Page
```

#### 2.2 Adicionar Região KPIs
```
Clique: + (Create Region)
Name: KPIs
Type: Static Content
Title: KPIs do Sistema
Clique: Create
```

#### 2.3 Adicionar Item 1: Vendas Hoje
```
Na região KPIs, clique: +
Name: P1_VENDAS_HOJE
Type: Value
Label: Vendas Hoje
SQL: SELECT NVL(SUM(valor_final),0) FROM VENDAS 
     WHERE TRUNC(data_venda)=TRUNC(SYSDATE) AND status='CONCLUIDA'
Format: Currency
Clique: Create
```

#### 2.4 Adicionar Item 2: Faturamento Mês
```
Clique: + (na região KPIs)
Name: P1_FATURAMENTO_MES
Type: Value
Label: Faturamento Mês
SQL: SELECT NVL(SUM(valor_final),0) FROM VENDAS 
     WHERE TRUNC(data_venda,'MM')=TRUNC(SYSDATE,'MM') AND status='CONCLUIDA'
Format: Currency
Clique: Create
```

#### 2.5 Adicionar Item 3: Produtos em Falta
```
Clique: + (na região KPIs)
Name: P1_PRODUTOS_FALTA
Type: Value
Label: Produtos em Falta
SQL: SELECT COUNT(*) FROM PRODUTOS 
     WHERE quantidade <= estoque_minimo AND ativo = 'S'
Format: Number
Clique: Create
```

#### 2.6 Adicionar Item 4: Clientes Ativos
```
Clique: + (na região KPIs)
Name: P1_CLIENTES_ATIVOS
Type: Value
Label: Clientes Ativos
SQL: SELECT COUNT(*) FROM CLIENTES WHERE ativo = 'S'
Format: Number
Clique: Create
```

#### 2.7 Gráfico 1: Vendas 7 Dias
```
Clique: + (Create Region)
Name: Gráfico Vendas
Type: Chart
Title: Vendas - Últimos 7 Dias
Chart Type: Line
SQL: SELECT * FROM DASHBOARD_VENDAS_7DIAS
Label: data_fmt
Value: total_vendido
Clique: Create
```

#### 2.8 Gráfico 2: Top 5 Produtos
```
Clique: + (Create Region)
Name: Gráfico Produtos
Type: Chart
Title: Produtos Mais Vendidos
Chart Type: Bar (Horizontal)
SQL: SELECT * FROM DASHBOARD_TOP_PRODUTOS WHERE ROWNUM <= 5
Label: nome
Value: qtd
Clique: Create
```

#### 2.9 Gráfico 3: Formas Pagamento
```
Clique: + (Create Region)
Name: Gráfico Pagamentos
Type: Chart
Title: Distribuição Pagamentos
Chart Type: Pie
SQL: SELECT * FROM DASHBOARD_PAGAMENTOS
Label: forma_pagamento
Value: qtd
Clique: Create
```

#### 2.10 Adicionar Alertas
```
Clique: + (Create Region)
Name: Alertas Estoque
Type: Interactive Grid
Title: ⚠️ Produtos em Falta
SQL: SELECT nome, quantidade, estoque_minimo FROM PRODUTOS 
     WHERE quantidade <= estoque_minimo AND ativo = 'S'
Read Only: Yes
Clique: Create
```

---

### PASSO 3: Testar (1 min)

```
1. Clique: Run Page (ou F10)
2. Verifique:
   ✓ KPIs aparecem
   ✓ Gráficos renderizam
   ✓ Alertas mostram dados
3. Pronto! 🎉
```

---

## 📊 Resultado

Sua página HOME terá:

```
┌────────────────────────────────────────┐
│ [Vendas]  [Faturamento] [Falta] [Clientes]
│ R$1,2k    R$15,6k           5      127
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ Gráfico Vendas │ Top Produtos │ Pagam  │
│ (Linha)        │ (Barras)     │ (Pizza)│
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ ⚠️ Produtos em Falta:
│ Água 1.5L: 5 de 50
│ Feijão: 8 de 20
└────────────────────────────────────────┘
```

---

## ⚠️ Problemas Comuns

**KPIs mostram 0?**
```sql
-- Insira dados de teste em SQL:
INSERT INTO VENDAS (cliente_id, valor_total, valor_final, forma_pagamento, status)
VALUES (1, 100, 100, 'DINHEIRO', 'CONCLUIDA');
COMMIT;
-- Clique "Refresh" na página
```

**Gráficos vazios?**
- Verifique se a view retorna dados em SQL
- Execute: `SELECT * FROM DASHBOARD_VENDAS_7DIAS;`

**Erro "View não existe"?**
- Volte ao PASSO 1
- Execute todas as views

---

## ✅ Checklist

- [ ] Views criadas em SQL
- [ ] Página 1 criada
- [ ] 4 KPIs adicionados
- [ ] 3 Gráficos adicionados
- [ ] Alertas adicionados
- [ ] Página testada
- [ ] Dados aparecem corretamente

---

## 📚 Para Mais Detalhes

Veja: `02_CREATE_HOME_PAGE.md`

---

**Tempo Total:** 15 minutos  
**Status:** Pronto para começar! 🚀
