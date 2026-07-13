# 🏗️ Guia Completo: Criar Sistema Todo em Oracle APEX

**Tempo Total:** 2-3 horas  
**Dificuldade:** Intermediária  
**Resultado:** Sistema de Gestão de Mercado 100% Funcional

---

## 📋 Visão Geral do Sistema

Você criará 8 páginas com 50+ componentes que funcionam juntos:

```
┌─────────────────────────────────────────┐
│ PÁGINA 1: HOME (Dashboard)              │
│ - 4 KPIs em cards                       │
│ - 3 Gráficos                            │
│ - 2 Alertas                             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PÁGINA 10-11: PRODUTOS (CRUD)           │
│ - Listar produtos com grid              │
│ - Criar/editar com formulário           │
│ - Categorias                            │
│ - Validações                            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PÁGINA 20-21: PDV (Ponto de Venda)      │
│ - Carrinho de compras                   │
│ - Busca rápida de produtos              │
│ - Confirmação de venda                  │
│ - Impressão de cupom                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PÁGINA 30: VENDAS (Histórico)           │
│ - Lista de vendas com filtros           │
│ - Detalhes de cada venda                │
│ - Devolução de vendas                   │
│ - Relatórios                            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PÁGINA 40: ESTOQUE (Gestão)             │
│ - Movimentações                         │
│ - Ajustes manuais                       │
│ - Alertas de estoque baixo              │
│ - Histórico completo                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PÁGINA 50: COMPRAS (Fornecedores)       │
│ - Pedidos de compra                     │
│ - Gestão de fornecedores                │
│ - Recebimento                           │
│ - Histórico                             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PÁGINA 110: CLIENTES (Gestão)           │
│ - Lista de clientes                     │
│ - Cadastro/edição                       │
│ - Histórico de compras                  │
│ - Crediário                             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PÁGINA 200: ADMIN (Configurações)       │
│ - Gestão de categorias                  │
│ - Gestão de usuários (futura)           │
│ - Relatórios administrativos            │
└─────────────────────────────────────────┘
```

---

## 📊 Pré-Requisitos

Você DEVE ter concluído:

- [x] Conta Oracle Cloud criada
- [x] Database MERCADO_DB provisionado
- [x] Script `01_CREATE_DATABASE_SCHEMA.sql` executado
- [x] Workspace MERCADO_FAMILIA criado
- [x] Aplicação "Sistema de Gestão de Mercado" criada
- [ ] Script `03_VIEWS_PROCEDURES_COMPLETO.sql` executado (faça agora!)

---

## 🚀 PASSO 1: Preparar o Banco (5 min)

### 1.1 Executar Script de Suporte

1. Abra: **SQL Developer Web**
2. Login: APEX_DEVELOPER
3. Execute o arquivo: **03_VIEWS_PROCEDURES_COMPLETO.sql**

```
Isto criará:
✓ 11 Views novas
✓ 7 Procedures novas
✓ Total: 18 objetos de suporte
```

4. Verifique se viu: "✓ Sistema pronto para APEX!"

---

## 🎯 PASSO 2: Criar Página 1 - HOME (15 min)

### 📖 Siga o Guia: `02_CREATE_HOME_PAGE.md` ou `GUIA_RAPIDO_HOME.md`

**Resultado esperado:**
```
✓ 4 Cards KPI (Vendas, Faturamento, Falta, Clientes)
✓ 3 Gráficos (Linha, Barras, Pizza)
✓ 2 Alertas (Estoque, Compras)
```

---

## 🏷️ PASSO 3: Criar Página 10 - Listar Produtos (15 min)

### 3.1 Criar Página

```
App Builder → Create → Blank Page
Page Number: 10
Page Name: PRODUTOS
Page Title: Gerenciar Produtos
```

### 3.2 Adicionar Região Principal

```
Create Region
Name: Produtos
Type: Interactive Grid
Title: Lista de Produtos

SQL:
SELECT * FROM V_PRODUTOS_COMPLETO
```

### 3.3 Configurar Colunas

```
Colunas a manter:
- produto_id (Hidden)
- nome (Text)
- sku (Text)
- categoria (Text)
- quantidade (Number)
- preco_venda (Currency)
- margem_percentual (Number)
- ativo (Checkbox)

Colunas a remover:
- Tudo que não está acima
```

### 3.4 Configurar Acões

```
Adicione botão: "Novo Produto"
Action: Navigate to Page
Target: 11

Adicione botão: "Editar"
Action: Edit Row
Target: Page 11
```

### 3.5 Adicionar Filtros

```
Add Filter:
- Label: Categoria
- Column: categoria
- Type: Select List

Add Filter:
- Label: Status
- Column: ativo
- Type: Checkbox
```

---

## 📝 PASSO 4: Criar Página 11 - Criar/Editar Produto (20 min)

### 4.1 Criar Página

```
App Builder → Create → Blank Page
Page Number: 11
Page Name: EDITAR_PRODUTO
Page Title: Criar/Editar Produto
```

### 4.2 Adicionar Região Formulário

```
Create Region
Name: Dados Produto
Type: Form
Title: Informações do Produto

SQL (Select):
SELECT * FROM PRODUTOS WHERE produto_id = :P11_PRODUTO_ID

SQL (Insert):
INSERT INTO PRODUTOS 
(categoria_id, nome, descricao, preco_custo, preco_venda, 
 quantidade, estoque_minimo, sku)
VALUES (:P11_CATEGORIA_ID, :P11_NOME, :P11_DESCRICAO, 
        :P11_PRECO_CUSTO, :P11_PRECO_VENDA, 
        :P11_QUANTIDADE, :P11_ESTOQUE_MINIMO, :P11_SKU)

SQL (Update):
UPDATE PRODUTOS SET
categoria_id = :P11_CATEGORIA_ID,
nome = :P11_NOME,
descricao = :P11_DESCRICAO,
preco_custo = :P11_PRECO_CUSTO,
preco_venda = :P11_PRECO_VENDA,
quantidade = :P11_QUANTIDADE,
estoque_minimo = :P11_ESTOQUE_MINIMO,
sku = :P11_SKU
WHERE produto_id = :P11_PRODUTO_ID
```

### 4.3 Adicionar Items ao Formulário

```
Items necessários:
- P11_PRODUTO_ID (Hidden)
- P11_CATEGORIA_ID (Select List - CATEGORIAS)
- P11_NOME (Text)
- P11_DESCRICAO (Textarea)
- P11_PRECO_CUSTO (Number)
- P11_PRECO_VENDA (Number)
- P11_QUANTIDADE (Number)
- P11_ESTOQUE_MINIMO (Number)
- P11_SKU (Text)
```

### 4.4 Adicionar Validações

```
P11_NOME: Not Null
P11_CATEGORIA_ID: Not Null
P11_PRECO_VENDA: > P11_PRECO_CUSTO
P11_SKU: Unique (PRODUTOS.sku)
```

### 4.5 Adicionar Botões

```
Botão: SALVAR
Action: Submit Form

Botão: VOLTAR
Action: Navigate to Page 10
```

---

## 💳 PASSO 5: Criar Página 20 - PDV (Carrinho) (25 min)

### 5.1 Criar Página

```
App Builder → Create → Blank Page
Page Number: 20
Page Name: PDV_CARRINHO
Page Title: Ponto de Venda
```

### 5.2 Região 1: Buscar Produto

```
Create Region
Name: Buscar Produto
Type: Static Content

Componentes:
- P20_BUSCA (Text) - Buscar por nome
- P20_CATEGORIA (Select) - Filtrar categoria
- Botão: Buscar
```

### 5.3 Região 2: Seleção de Produtos

```
Create Region
Name: Produtos Disponíveis
Type: Interactive Grid

SQL:
SELECT produto_id, nome, sku, preco_venda, quantidade
FROM PRODUTOS
WHERE ativo = 'S' AND quantidade > 0
AND (nome LIKE '%' || :P20_BUSCA || '%' OR :P20_BUSCA IS NULL)
AND (categoria_id = :P20_CATEGORIA OR :P20_CATEGORIA IS NULL)
```

### 5.4 Região 3: Carrinho

```
Create Region
Name: Carrinho
Type: Interactive Grid

SQL:
SELECT item_venda_id, produto_id, nome, quantidade, 
       preco_unitario, desconto_item, subtotal
FROM ITENS_VENDA
WHERE venda_id = :P20_VENDA_ID
```

### 5.5 Região 4: Resumo da Venda

```
Items:
- P20_VALOR_TOTAL (Display) - SQL: SELECT valor_total FROM VENDAS WHERE venda_id = :P20_VENDA_ID
- P20_DESCONTO (Number) - Input
- P20_VALOR_FINAL (Display) - Calculado
- P20_FORMA_PAGAMENTO (Select) - DINHEIRO, CARTAO_CREDITO, PIX, etc
```

### 5.6 Botões

```
Botão: INICIAR VENDA
- Call Procedure: SP_CRIAR_VENDA
- Return variable: P20_VENDA_ID

Botão: ADICIONAR AO CARRINHO
- Call Procedure: SP_ADICIONAR_ITEM_VENDA
- Refresh Carrinho

Botão: REMOVER ITEM
- Delete from ITENS_VENDA

Botão: FINALIZAR
- Navigate to Page 21
```

---

## ✅ PASSO 6: Criar Página 21 - PDV (Confirmação) (15 min)

### 6.1 Criar Página

```
App Builder → Create → Blank Page
Page Number: 21
Page Name: PDV_CONFIRMACAO
Page Title: Confirmação de Venda
```

### 6.2 Região: Resumo

```
Create Region
Name: Resumo Venda
Type: Static Content

Displays:
- Itens vendidos
- Valor total
- Desconto
- Valor final
- Forma de pagamento
```

### 6.3 Items

```
- P21_VENDA_ID (Hidden)
- P21_CLIENTE_ID (Select) - CLIENTES
- P21_VALOR_FINAL (Display)
- P21_FORMA_PAGAMENTO (Display)
```

### 6.4 Botões

```
Botão: CONFIRMAR VENDA
- Call Procedure: SP_FINALIZAR_VENDA
- After Success: Print/Show Message

Botão: CANCELAR
- Call Procedure: SP_CANCELAR_VENDA
- Navigate to Page 20

Botão: NOVO CLIENTE
- Navigate to Page 110 (Clientes)
```

---

## 📋 PASSO 7: Criar Página 30 - Vendas (Histórico) (20 min)

### 7.1 Criar Página

```
App Builder → Create → Blank Page
Page Number: 30
Page Name: VENDAS
Page Title: Histórico de Vendas
```

### 7.2 Região: Lista de Vendas

```
Create Region
Name: Vendas
Type: Interactive Grid

SQL:
SELECT * FROM V_VENDAS_DETALHADO
```

### 7.3 Adicionar Filtros

```
- Data (Date Range)
- Cliente (Select)
- Status (Select)
- Forma de Pagamento (Select)
```

### 7.4 Ações

```
Botão: VER DETALHES
- Navigate to Page 31

Botão: DEVOLVER
- Call Procedure: SP_CANCELAR_VENDA
```

---

## 📊 PASSO 8: Criar Página 40 - Estoque (20 min)

### 8.1 Criar Página

```
App Builder → Create → Blank Page
Page Number: 40
Page Name: ESTOQUE
Page Title: Gestão de Estoque
```

### 8.2 Região 1: Status Estoque

```
Create Region
Name: Produtos por Status
Type: Interactive Grid

SQL:
SELECT * FROM V_ESTOQUE_STATUS
```

### 8.3 Região 2: Fazer Ajuste

```
Create Region
Name: Ajustar Estoque
Type: Form

Items:
- P40_PRODUTO_ID (Select)
- P40_QUANTIDADE (Number)
- P40_MOTIVO (Text)

Botão: AJUSTAR
- Call Procedure: SP_AJUSTAR_ESTOQUE
```

### 8.4 Região 3: Histórico

```
Create Region
Name: Movimentações
Type: Interactive Grid

SQL:
SELECT * FROM V_MOVIMENTACOES_DETALHADO
ORDER BY criada_em DESC
```

---

## 🛒 PASSO 9: Criar Página 50 - Compras (20 min)

### 9.1 Criar Página

```
App Builder → Create → Blank Page
Page Number: 50
Page Name: COMPRAS
Page Title: Gestão de Compras
```

### 9.2 Região 1: Lista de Compras

```
Create Region
Name: Compras
Type: Interactive Grid

SQL:
SELECT * FROM V_COMPRAS_DETALHADO
```

### 9.3 Região 2: Criar Compra

```
Create Region
Name: Nova Compra
Type: Form

Items:
- P50_COMPRA_ID (Hidden)
- P50_FORNECEDOR_ID (Select)
- P50_DATA_ENTREGA (Date)

Botão: CRIAR
- Call Procedure: SP_CRIAR_COMPRA
```

### 9.4 Região 3: Itens da Compra

```
Create Region
Name: Itens
Type: Interactive Grid

SQL:
SELECT * FROM V_ITENS_COMPRA_DETALHADO
WHERE compra_id = :P50_COMPRA_ID
```

### 9.5 Ações

```
Botão: RECEBER COMPRA
- Call Procedure: SP_RECEBER_COMPRA

Botão: CANCELAR
- Update COMPRAS status = 'CANCELADA'
```

---

## 👥 PASSO 10: Criar Página 110 - Clientes (20 min)

### 10.1 Criar Página

```
App Builder → Create → Blank Page
Page Number: 110
Page Name: CLIENTES
Page Title: Gestão de Clientes
```

### 10.2 Região 1: Lista de Clientes

```
Create Region
Name: Clientes
Type: Interactive Grid

SQL:
SELECT * FROM V_CLIENTES_COMPLETO
```

### 10.3 Região 2: Criar/Editar Cliente

```
Create Region
Name: Dados Cliente
Type: Form

Items (semelhante ao de Produtos):
- P110_CLIENTE_ID
- P110_NOME
- P110_CPF
- P110_EMAIL
- P110_TELEFONE
- P110_ENDERECO
- P110_CIDADE
- P110_ESTADO
- P110_CEP
- P110_TIPO (FISICO/JURIDICO)
```

### 10.4 Validações

```
- P110_NOME: Not Null
- P110_CPF: Unique
- P110_EMAIL: Unique
```

---

## ⚙️ PASSO 11: Criar Página 200 - Admin (15 min)

### 11.1 Criar Página

```
App Builder → Create → Blank Page
Page Number: 200
Page Name: ADMIN
Page Title: Administração
```

### 11.2 Região 1: Categorias

```
Create Region
Name: Categorias
Type: Interactive Grid

SQL:
SELECT categoria_id, nome, descricao, ativa, criada_em
FROM CATEGORIAS
ORDER BY nome
```

Adicione:
- Botão: Nova Categoria
- Botão: Editar
- Botão: Ativar/Desativar

### 11.3 Região 2: Fornecedores

```
Create Region
Name: Fornecedores
Type: Interactive Grid

SQL:
SELECT * FROM V_FORNECEDORES_COMPLETO
```

---

## 📊 PASSO 12: Criar Relatórios (15 min)

Adicione à página 200 ou crie página 300:

```
Relatório 1: Vendas por Período
SELECT * FROM V_VENDAS_PERIODO

Relatório 2: Lucro por Produto
SELECT * FROM V_LUCRO_PRODUTO

Relatório 3: Estoque Crítico
SELECT * FROM V_ESTOQUE_STATUS WHERE status_estoque = 'CRÍTICO'
```

---

## 🎯 Checklist Final

```
Preparação:
- [ ] Views e Procedures criadas (PASSO 1)

Páginas Criadas:
- [ ] Página 1: HOME (Dashboard)
- [ ] Página 10: Listar Produtos
- [ ] Página 11: Criar/Editar Produto
- [ ] Página 20: PDV Carrinho
- [ ] Página 21: PDV Confirmação
- [ ] Página 30: Histórico Vendas
- [ ] Página 40: Gestão Estoque
- [ ] Página 50: Compras
- [ ] Página 110: Gestão Clientes
- [ ] Página 200: Admin

Funcionalidades:
- [ ] CRUD Produtos
- [ ] CRUD Clientes
- [ ] PDV Funcional
- [ ] Histórico Vendas
- [ ] Gestão Estoque
- [ ] Compras
- [ ] Gráficos no Dashboard
- [ ] Filtros em Grids
- [ ] Validações
- [ ] Relatórios
```

---

## 💡 Dicas Importantes

### Dica 1: Salve Frequentemente
Use Ctrl+S após cada mudança importante.

### Dica 2: Teste Enquanto Constrói
Execute a página depois de adicionar cada região.

### Dica 3: Use Templates
APEX tem templates prontos - personalize-os.

### Dica 4: Dados de Teste
Sempre teste com dados reais antes de usar em produção.

### Dica 5: Validações
Adicione validações em TODOS os formulários.

---

## 🚨 Troubleshooting

### Problema: Grid não mostra dados
```
✓ Verifique a query em SQL Developer
✓ Certifique-se de que a view/tabela existe
✓ Verifique se há dados para mostrar
```

### Problema: Botão não funciona
```
✓ Verifique a ação do botão
✓ Certifique-se de que os items estão nomeados corretamente
✓ Verifique se as procedures existem
```

### Problema: Validação não funciona
```
✓ Certifique-se de que o tipo de validação é correto
✓ Verifique o nome do item
✓ Teste a validação SQL em SQL Developer
```

---

## ⏱️ Timeline Estimada

```
PASSO 1:  Preparar Banco      ~  5 min
PASSO 2:  HOME                ~ 15 min
PASSO 3:  Produtos (Listar)   ~ 15 min
PASSO 4:  Produtos (Criar)    ~ 20 min
PASSO 5:  PDV (Carrinho)      ~ 25 min
PASSO 6:  PDV (Confirmação)   ~ 15 min
PASSO 7:  Vendas              ~ 20 min
PASSO 8:  Estoque             ~ 20 min
PASSO 9:  Compras             ~ 20 min
PASSO 10: Clientes            ~ 20 min
PASSO 11: Admin               ~ 15 min
PASSO 12: Relatórios          ~ 15 min
─────────────────────────────────────
TOTAL: ~205 min = 3,5 horas aprox
```

**Versão realista:** 3-4 horas com testes

---

## 📚 Recursos Úteis

- [APEX Page Designer Docs](https://docs.oracle.com/en/database/oracle/apex/)
- [Interactive Grid](https://docs.oracle.com/en/database/oracle/apex/21.1/htmdb/using-interactive-grids.html)
- [Forms](https://docs.oracle.com/en/database/oracle/apex/21.1/htmdb/using-form-pages.html)
- [Charts](https://docs.oracle.com/en/database/oracle/apex/21.1/htmdb/using-charts.html)

---

## ✅ Após Completar

Você terá:
- ✅ Sistema completo funcional
- ✅ 8 páginas APEX
- ✅ 50+ componentes
- ✅ 11 views + 7 procedures
- ✅ CRUD completo
- ✅ PDV funcional
- ✅ Dashboards com dados reais
- ✅ Pronto para usar em produção (com ajustes)

---

**Versão:** 1.0  
**Data:** Julho 2026  
**Status:** Pronto para Implementar

Bom trabalho! 🚀
