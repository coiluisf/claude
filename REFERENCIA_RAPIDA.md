# 📚 Referência Rápida - Sistema de Mercado APEX

**Use este arquivo como consulta rápida durante o desenvolvimento.**

---

## 🔐 Credenciais e URLs

### Oracle Cloud
```
URL Console: https://cloud.oracle.com
Database: MERCADO_DB
Região: (sua região escolhida)
```

### Database (SQL Developer Web)
```
URL: https://[seu-instance].adb.[região].oraclecloud.com/ords/sql
Username: ADMIN
Password: SenhaSegura123!@
```

### APEX - Workspace INTERNAL (Admin)
```
URL: https://[seu-instance].adb.[região].oraclecloud.com/ords/apex
Workspace: INTERNAL
Username: ADMIN
Password: SenhaSegura123!@
```

### APEX - Workspace MERCADO_FAMILIA (Desenvolvimento)
```
URL: https://[seu-instance].adb.[região].oraclecloud.com/ords/apex
Workspace: MERCADO_FAMILIA
Username: APEX_DEVELOPER
Password: SenhaAPEX123!@
```

---

## 🛠️ Tabelas Principais

### CATEGORIAS
```sql
-- Inserir categoria
INSERT INTO CATEGORIAS (nome, descricao, ativa)
VALUES ('Alimentos', 'Produtos alimentares', 'S');

-- Listar todas
SELECT * FROM CATEGORIAS;
```

### PRODUTOS
```sql
-- Inserir produto
INSERT INTO PRODUTOS (categoria_id, nome, preco_custo, preco_venda, quantidade, sku, ativo)
VALUES (1, 'Arroz 5kg', 15.00, 24.90, 50, 'ARR-001', 'S');

-- Listar produtos
SELECT * FROM PRODUTOS ORDER BY nome;

-- Produtos em falta
SELECT * FROM PRODUTOS WHERE quantidade <= estoque_minimo;
```

### VENDAS e ITENS_VENDA
```sql
-- Criar venda
INSERT INTO VENDAS (cliente_id, valor_total, valor_final, forma_pagamento, status)
VALUES (1, 100.00, 100.00, 'DINHEIRO', 'CONCLUIDA');

-- Adicionar itens
INSERT INTO ITENS_VENDA (venda_id, produto_id, quantidade, preco_unitario, subtotal)
VALUES (1, 1, 2, 24.90, 49.80);

-- Ver vendas
SELECT * FROM VENDAS ORDER BY data_venda DESC;

-- Ver itens de uma venda
SELECT iv.*, p.nome 
FROM ITENS_VENDA iv
JOIN PRODUTOS p ON iv.produto_id = p.produto_id
WHERE iv.venda_id = 1;
```

### CLIENTES
```sql
-- Inserir cliente
INSERT INTO CLIENTES (nome, cpf, email, telefone, tipo, ativo)
VALUES ('João Silva', '12345678901', 'joao@email.com', '11987654321', 'FISICO', 'S');

-- Listar clientes ativos
SELECT * FROM CLIENTES WHERE ativo = 'S';

-- Ver compras de um cliente
SELECT c.nome, COUNT(v.venda_id) as qtd_compras, SUM(v.valor_final) as total_gasto
FROM CLIENTES c
LEFT JOIN VENDAS v ON c.cliente_id = v.cliente_id
WHERE c.cliente_id = 1
GROUP BY c.cliente_id, c.nome;
```

### MOVIMENTAÇÕES_ESTOQUE
```sql
-- Registrar entrada
INSERT INTO MOVIMENTACOES_ESTOQUE 
(produto_id, tipo_movimento, quantidade, motivo)
VALUES (1, 'ENTRADA', 50, 'Compra do fornecedor ABC');

-- Ver histórico de um produto
SELECT * FROM MOVIMENTACOES_ESTOQUE
WHERE produto_id = 1
ORDER BY criada_em DESC;
```

---

## 📊 Views Principais

### PRODUTOS_COM_ALERTA
```sql
-- Ver produtos com alerta de estoque
SELECT * FROM PRODUTOS_COM_ALERTA;

-- Filtra por status
SELECT * FROM PRODUTOS_COM_ALERTA WHERE status_estoque = 'CRÍTICO';
```

### VENDAS_DIARIAS
```sql
-- Ver vendas por dia
SELECT * FROM VENDAS_DIARIAS;

-- Faturamento total este mês
SELECT SUM(total_vendido) as faturamento_total FROM VENDAS_DIARIAS
WHERE data >= TRUNC(SYSDATE, 'MM');
```

### PRODUTOS_MAIS_VENDIDOS
```sql
-- Ver produtos mais vendidos
SELECT * FROM PRODUTOS_MAIS_VENDIDOS WHERE ROWNUM <= 10;
```

### SALDO_CLIENTES
```sql
-- Ver clientes que mais compraram
SELECT * FROM SALDO_CLIENTES ORDER BY total_gasto DESC;
```

---

## 🔄 Procedures Disponíveis

### FINALIZAR_VENDA
```sql
-- Finalizar uma venda
DECLARE
  v_status VARCHAR2(200);
BEGIN
  FINALIZAR_VENDA(venda_id => 1, p_status => v_status);
  DBMS_OUTPUT.PUT_LINE(v_status);
END;
/
```

---

## 📝 Queries Úteis

### Dashboard - KPIs do Dia
```sql
SELECT
  TRUNC(SYSDATE) as data,
  COUNT(DISTINCT venda_id) as qtd_vendas,
  SUM(valor_final) as faturamento,
  AVG(valor_final) as ticket_medio
FROM VENDAS
WHERE TRUNC(data_venda) = TRUNC(SYSDATE);
```

### Produtos com Estoque Crítico
```sql
SELECT produto_id, nome, quantidade, estoque_minimo
FROM PRODUTOS
WHERE quantidade <= estoque_minimo
AND ativo = 'S'
ORDER BY quantidade ASC;
```

### Margem de Lucro por Produto
```sql
SELECT 
  nome,
  preco_custo,
  preco_venda,
  ROUND(((preco_venda - preco_custo) / preco_custo * 100), 2) as margem_percentual,
  (preco_venda - preco_custo) as margem_valor
FROM PRODUTOS
WHERE ativo = 'S'
ORDER BY margem_percentual DESC;
```

### Clientes Inativos (sem compras)
```sql
SELECT c.cliente_id, c.nome, c.email
FROM CLIENTES c
LEFT JOIN VENDAS v ON c.cliente_id = v.cliente_id
WHERE c.ativo = 'S'
AND v.venda_id IS NULL;
```

### Top 5 Fornecedores
```sql
SELECT 
  f.fornecedor_id, f.nome,
  COUNT(c.compra_id) as qtd_compras,
  SUM(c.valor_total) as valor_total
FROM FORNECEDORES f
LEFT JOIN COMPRAS c ON f.fornecedor_id = c.fornecedor_id
WHERE f.ativo = 'S'
GROUP BY f.fornecedor_id, f.nome
ORDER BY valor_total DESC;
```

### Tickets de Venda por Forma de Pagamento
```sql
SELECT 
  forma_pagamento,
  COUNT(*) as qtd_vendas,
  AVG(valor_final) as ticket_medio,
  SUM(valor_final) as total_vendido
FROM VENDAS
WHERE status = 'CONCLUIDA'
GROUP BY forma_pagamento
ORDER BY total_vendido DESC;
```

---

## ⚡ Atalhos Úteis

### SQL Developer Web
```
Ctrl+Enter       → Executar SQL
Ctrl+A           → Selecionar tudo
Ctrl+C           → Copiar
Ctrl+V           → Colar
Ctrl+Z           → Desfazer
Ctrl+Shift+Delete → Limpar histórico
```

### APEX App Builder
```
F2               → Renomear página
Delete           → Deletar elemento
Ctrl+S           → Salvar
F12              → Developer Tools
```

---

## 🎨 IDs de Páginas APEX (Convenção)

```
1   → HOME (Dashboard)
10  → Produtos (Listar)
11  → Produtos (Editar/Criar)
20  → PDV (Carrinho)
21  → PDV (Confirmação)
30  → Vendas (Listar)
31  → Vendas (Detalhe)
40  → Estoque (Movimentações)
50  → Compras (Gestão)
100 → Relatórios
110 → Clientes
200 → Admin
```

---

## 📦 Estrutura de Pastas (Futura)

```
projeto-mercado-apex/
├── README.md
├── GUIA_SETUP_PASSO_A_PASSO.md
├── PROJETO_MERCADO_APEX.md
├── REFERENCIA_RAPIDA.md
│
├── sql/
│   ├── 01_CREATE_DATABASE_SCHEMA.sql
│   ├── 02_CREATE_APEX_PAGES.sql
│   ├── 03_TRIGGERS_AUTOMACAO.sql
│   └── 04_RELATORIOS_SQL.sql
│
├── apex/
│   ├── PAGE_1_HOME.sql
│   ├── PAGE_10_PRODUTOS.sql
│   ├── PAGE_20_PDV.sql
│   └── ...
│
├── exports/
│   └── system-backup.sql
│
└── docs/
    ├── ARQUITETURA.md
    ├── FLUXOS.md
    └── TROUBLESHOOTING.md
```

---

## 🔄 Workflow Típico de Desenvolvimento

### 1. Preparar Dados
```sql
-- SQL Developer Web
INSERT INTO CATEGORIAS (...) VALUES (...);
COMMIT;
```

### 2. Testar Query
```sql
-- SQL Developer Web
SELECT * FROM PRODUTOS;
```

### 3. Criar Página APEX
```
APEX App Builder
→ Create Page
→ Interactive Grid / Form
→ Conectar à tabela
```

### 4. Configurar Componentes
```
Componentes → Editar Propriedades
- Labels
- Validações
- Ações
- Estilos
```

### 5. Testar e Deploy
```
Run Application
Testar fluxos
Fazer ajustes
Salvar alterações
```

---

## 🐛 Debug e Troubleshooting

### Verificar Status da Aplicação
```sql
-- Em SQL
SELECT * FROM APEX_APPLICATIONS
WHERE application_name = 'Sistema de Gestão de Mercado';
```

### Limpar Cache APEX
```
Navegador: Ctrl+Shift+Delete
APEX: Application Settings → Clear Cache
```

### Ver Logs de Erro
```
APEX: Administration → Logs → View Logs
Procure por timestamps recentes
```

### Resetar Sequências
```sql
-- Se auto-incremento parar
ALTER SEQUENCE SEQ_PRODUTOS RESTART START WITH 1;
```

---

## 📞 Comandos Rápidos

### Conectar ao Banco
```bash
# Via SSH (se tiver acesso)
sqlplus admin@mercado_db
```

### Fazer Backup
```sql
-- Oracle Data Pump
EXPDP admin/password@mercado_db DIRECTORY=DATA_PUMP_DIR 
DUMPFILE=mercado_backup.dmp LOGFILE=mercado_backup.log;
```

### Verificar Espaço
```sql
SELECT tablespace_name, SUM(bytes)/1024/1024 as MB
FROM dba_segments
GROUP BY tablespace_name;
```

---

## 📈 Performance - Índices Recomendados

```sql
-- Melhorar queries de produtos
CREATE INDEX idx_produtos_categoria ON PRODUTOS(categoria_id);
CREATE INDEX idx_produtos_sku ON PRODUTOS(sku);

-- Melhorar queries de vendas
CREATE INDEX idx_vendas_data ON VENDAS(data_venda);
CREATE INDEX idx_vendas_cliente ON VENDAS(cliente_id);

-- Melhorar queries de itens
CREATE INDEX idx_itens_venda_id ON ITENS_VENDA(venda_id);
CREATE INDEX idx_itens_produto_id ON ITENS_VENDA(produto_id);
```

---

## 🎓 Dicas de Desenvolvimento APEX

### 1. Nomes de Componentes
```
Use convenção: p_[nome] para páginas
               i_[nome] para itens
               r_[nome] para regiões
               b_[nome] para botões
```

### 2. Validações
```
Sempre validar entrada
- Não deixar campos vazios
- Validar formatos (CPF, CNPJ, etc)
- Limpar dados especiais
```

### 3. Mensagens de Feedback
```
SUCCESS   → Operação concluída
WARNING   → Atenção
ERROR     → Erro crítico
INFO      → Informação
```

### 4. Segurança
```
- Sempre usar bind variables
- Validar permissões
- Logar ações importantes
- Proteger dados sensíveis
```

---

## 🚀 Comandos Úteis

### Criar backup quick
```sql
BEGIN
  DBMS_OUTPUT.PUT_LINE('Backup em ' || SYSDATE);
  -- Seus comandos de backup
END;
/
```

### Contar registros
```sql
SELECT 'CATEGORIAS' as tabela, COUNT(*) as registros FROM CATEGORIAS
UNION ALL
SELECT 'PRODUTOS', COUNT(*) FROM PRODUTOS
UNION ALL
SELECT 'CLIENTES', COUNT(*) FROM CLIENTES
UNION ALL
SELECT 'VENDAS', COUNT(*) FROM VENDAS;
```

### Listar todas as tabelas
```sql
SELECT table_name FROM user_tables ORDER BY table_name;
```

---

## 📋 Checklist de Desenvolvimento

- [ ] Banco de dados em produção
- [ ] Dados de exemplo inseridos
- [ ] Views criadas e testadas
- [ ] Triggers funcionando
- [ ] Páginas APEX criadas
- [ ] Componentes conectados
- [ ] Validações implementadas
- [ ] Mensagens de sucesso/erro
- [ ] Testes de fluxo completos
- [ ] Backup configurado
- [ ] Documentação atualizada

---

## 🆘 Ayuda Rápida

**Tabela não aparece?**
```sql
SELECT * FROM user_tables WHERE table_name = 'PRODUTOS';
```

**Erro de permissão?**
```sql
-- Como ADMIN
GRANT ALL ON PRODUTOS TO APEX_DEVELOPER;
```

**Sequence não funciona?**
```sql
SELECT SEQ_PRODUTOS.NEXTVAL FROM DUAL;
```

**Trigger disparou erro?**
```sql
-- Ver triggers
SELECT trigger_name FROM user_triggers WHERE table_name = 'PRODUTOS';
```

---

## 📚 Links Úteis

- [Oracle APEX Docs](https://docs.oracle.com/en/database/oracle/apex/)
- [Oracle SQL Reference](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/)
- [PL/SQL Guide](https://docs.oracle.com/en/database/oracle/oracle-database/23/lnpls/)
- [Oracle Cloud Docs](https://docs.oracle.com/en-us/iaas/Content/home.htm)

---

**Versão:** 1.0  
**Data:** Julho 2026  
**Status:** Pronto para usar
