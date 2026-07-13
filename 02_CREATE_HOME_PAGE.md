# 🏠 Guia: Criar Página HOME (Dashboard)

**Página:** 1  
**Nome:** HOME  
**Descrição:** Dashboard executivo com KPIs e gráficos  
**Tempo Estimado:** 20-30 minutos

---

## 📋 Visão Geral da Página HOME

A página HOME será o primeiro lugar que os usuários veem ao abrir a aplicação. Deve conter:

- 📊 **4 Cards de KPI** (Topo)
  - Vendas de Hoje
  - Total Faturado (Mês)
  - Produtos em Falta
  - Clientes Ativos

- 📈 **Gráficos** (Centro)
  - Gráfico de Vendas (Últimos 7 dias)
  - Gráfico de Produtos Mais Vendidos
  - Gráfico de Formas de Pagamento

- ⚠️ **Alertas** (Rodapé)
  - Produtos com estoque crítico
  - Compras pendentes

---

## 🎯 Passo 1: Criar a Página Base

### 1.1 Acessar App Builder
1. Faça login em seu workspace APEX
2. Clique em **"App Builder"**
3. Abra sua aplicação: **"Sistema de Gestão de Mercado"**

### 1.2 Editar Página 1 (ou Criar Nova)
1. Se você já tem uma página padrão, clique em **"1"** para editá-la
2. Se não, clique em **"+"** para criar uma página
3. Selecione: **"Blank Page"**
4. Configure:
   - **Page Number:** 1
   - **Page Name:** HOME
   - **Page Title:** Home

### 1.3 Salvar Página
1. Clique em **"Create Page"** ou **"Save"**
2. Você será levado ao editor da página

---

## 🎨 Passo 2: Adicionar Região Inicial

### 2.1 Criar Primeira Região (KPIs Topo)
1. No editor, procure por **"Regions"** ou **"+"**
2. Clique em **"Create Region"**
3. Configure:
   - **Name:** KPIs Topo
   - **Type:** Static Content
   - **Title:** KPIs do Sistema
   - **Position:** Body
4. Clique **"Create Region"**

### 2.2 Você está pronto para adicionar componentes!

---

## 📊 Passo 3: Adicionar Cards de KPI

### 3.1 Adicionar Item 1 - Vendas de Hoje

1. Na região "KPIs Topo", clique em **"+"** ou **"Create Item"**
2. Configure:
   - **Item Name:** P1_VENDAS_HOJE
   - **Type:** Value
   - **Label:** Vendas Hoje
   - **SQL Query:** 
```sql
SELECT SUM(valor_final) FROM VENDAS 
WHERE TRUNC(data_venda) = TRUNC(SYSDATE) 
AND status = 'CONCLUIDA'
```
   - **Format:** Currency
   - **CSS Classes:** Adicione estilo de card

3. Clique **"Create"**

### 3.2 Adicionar Item 2 - Faturamento Mês

1. Clique em **"+"** novamente
2. Configure:
   - **Item Name:** P1_FATURAMENTO_MES
   - **Type:** Value
   - **Label:** Faturamento (Mês)
   - **SQL Query:**
```sql
SELECT SUM(valor_final) FROM VENDAS 
WHERE TRUNC(data_venda, 'MM') = TRUNC(SYSDATE, 'MM')
AND status = 'CONCLUIDA'
```
   - **Format:** Currency

3. Clique **"Create"**

### 3.3 Adicionar Item 3 - Produtos em Falta

1. Clique em **"+"**
2. Configure:
   - **Item Name:** P1_PRODUTOS_FALTA
   - **Type:** Value
   - **Label:** Produtos em Falta
   - **SQL Query:**
```sql
SELECT COUNT(*) FROM PRODUTOS 
WHERE quantidade <= estoque_minimo 
AND ativo = 'S'
```
   - **Format:** Number
   - **Icon:** ⚠️ warning-circle

3. Clique **"Create"**

### 3.4 Adicionar Item 4 - Clientes Ativos

1. Clique em **"+"**
2. Configure:
   - **Item Name:** P1_CLIENTES_ATIVOS
   - **Type:** Value
   - **Label:** Clientes Ativos
   - **SQL Query:**
```sql
SELECT COUNT(*) FROM CLIENTES WHERE ativo = 'S'
```
   - **Format:** Number
   - **Icon:** 👥 users

3. Clique **"Create"**

---

## 📈 Passo 4: Adicionar Gráficos

### 4.1 Gráfico 1 - Vendas Últimos 7 Dias

1. Crie uma nova **Região:**
   - **Name:** Gráfico Vendas 7 Dias
   - **Type:** Chart
   - **Title:** Vendas - Últimos 7 Dias

2. Configure a Query:
```sql
SELECT 
  TO_CHAR(data_venda, 'DD/MM') as data,
  SUM(valor_final) as total
FROM VENDAS
WHERE data_venda >= TRUNC(SYSDATE) - 7
AND status = 'CONCLUIDA'
GROUP BY TRUNC(data_venda), TO_CHAR(data_venda, 'DD/MM')
ORDER BY data_venda
```

3. Configure o Gráfico:
   - **Chart Type:** Line (Linha)
   - **Label Column:** data
   - **Value Column:** total
   - **Display:** Com grid

4. Clique **"Create"**

### 4.2 Gráfico 2 - Produtos Mais Vendidos

1. Crie uma nova Região:
   - **Name:** Top 5 Produtos
   - **Type:** Chart
   - **Title:** Produtos Mais Vendidos

2. Configure a Query:
```sql
SELECT nome, quantidade_vendida
FROM PRODUTOS_MAIS_VENDIDOS
WHERE ROWNUM <= 5
ORDER BY quantidade_vendida DESC
```

3. Configure o Gráfico:
   - **Chart Type:** Bar (Horizontal)
   - **Label Column:** nome
   - **Value Column:** quantidade_vendida

4. Clique **"Create"**

### 4.3 Gráfico 3 - Formas de Pagamento

1. Crie uma nova Região:
   - **Name:** Pagamentos
   - **Type:** Chart
   - **Title:** Distribuição de Pagamentos

2. Configure a Query:
```sql
SELECT 
  forma_pagamento,
  COUNT(*) as quantidade,
  SUM(valor_final) as total
FROM VENDAS
WHERE status = 'CONCLUIDA'
AND data_venda >= TRUNC(SYSDATE) - 30
GROUP BY forma_pagamento
```

3. Configure o Gráfico:
   - **Chart Type:** Pie (Pizza)
   - **Label Column:** forma_pagamento
   - **Value Column:** quantidade

4. Clique **"Create"**

---

## ⚠️ Passo 5: Adicionar Alertas

### 5.1 Alertas de Estoque Crítico

1. Crie uma nova Região:
   - **Name:** Alertas Estoque
   - **Type:** Interactive Grid (ou Table)
   - **Title:** ⚠️ Produtos em Falta

2. Configure a Query:
```sql
SELECT 
  produto_id,
  nome,
  quantidade,
  estoque_minimo,
  categoria_id
FROM PRODUTOS
WHERE quantidade <= estoque_minimo
AND ativo = 'S'
ORDER BY quantidade ASC
```

3. Configure as Colunas:
   - **produto_id:** Hidden
   - **nome:** Text (Produto)
   - **quantidade:** Number (Qtd. Atual)
   - **estoque_minimo:** Number (Mínimo)
   - **categoria_id:** Hidden

4. Clique **"Create"**

### 5.2 Compras Pendentes

1. Crie uma nova Região:
   - **Name:** Compras Pendentes
   - **Type:** Interactive Grid (ou Table)
   - **Title:** 📦 Compras Pendentes

2. Configure a Query:
```sql
SELECT 
  c.compra_id,
  f.nome as fornecedor,
  c.valor_total,
  c.data_compra
FROM COMPRAS c
JOIN FORNECEDORES f ON c.fornecedor_id = f.fornecedor_id
WHERE c.status = 'PENDENTE'
ORDER BY c.data_compra
```

3. Configure as Colunas:
   - **compra_id:** Hidden
   - **fornecedor:** Text
   - **valor_total:** Currency
   - **data_compra:** Date

4. Clique **"Create"**

---

## 🎨 Passo 6: Personalizar Layout

### 6.1 Organizar Regiões em Colunas

1. No editor de página, vá para **"Layout"** ou **"Page Template"**
2. As regiões devem estar organizadas assim:

```
[KPIs - 4 itens lado a lado]

[Gráfico Vendas] [Gráfico Produtos] [Gráfico Pagamento]

[Alertas Estoque]

[Compras Pendentes]
```

3. Se necessário, ajuste as posições das regiões

### 6.2 Adicionar CSS Customizado (Opcional)

1. Vá para **"Page Designer"** > **"Styles"** ou **"CSS"**
2. Adicione:
```css
/* Cards de KPI */
.kpi-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: 10px;
}

.kpi-value {
  font-size: 32px;
  font-weight: bold;
  margin: 10px 0;
}

.kpi-label {
  font-size: 14px;
  opacity: 0.9;
}

/* Alertas */
.alert-critical {
  background-color: #fee;
  border-left: 4px solid #c33;
}

.alert-warning {
  background-color: #ffeaa7;
  border-left: 4px solid #fdcb6e;
}
```

3. Clique **"Apply Styles"**

---

## 🔄 Passo 7: Adicionar Comportamentos

### 7.1 Adicionar Botão "Atualizar"

1. Crie um novo **Item:**
   - **Name:** P1_BTN_ATUALIZAR
   - **Type:** Button
   - **Label:** ↻ Atualizar Dashboard
   - **Position:** Buttons

2. Configure a Ação:
   - **Action:** Refresh Page
   - **Refresh:** All
   - **Show Loading Indicator:** Yes

3. Clique **"Create"**

### 7.2 Adicionar Breadcrumb (Opcional)

1. Na página, procure por **"Breadcrumb"** ou **"Page Template"**
2. Adicione:
```
Home
```

---

## 🧪 Passo 8: Testar a Página

### 8.1 Salvar Mudanças
1. Clique em **"Save"** (Ctrl+S)
2. Aguarde a confirmação

### 8.2 Executar Página
1. Clique em **"Run Page"** (ou F10)
2. Uma nova aba abrirá com sua página
3. Verifique:
   - [ ] KPIs aparecem corretamente
   - [ ] Números estão corretos
   - [ ] Gráficos renderizam
   - [ ] Alertas mostram dados
   - [ ] Botão "Atualizar" funciona

### 8.3 Testando KPIs
```
Abra SQL Developer Web
Insira uma venda de teste:

INSERT INTO VENDAS (cliente_id, valor_total, valor_final, forma_pagamento, status)
VALUES (1, 50.00, 50.00, 'DINHEIRO', 'CONCLUIDA');
COMMIT;

Volte ao dashboard e clique "Atualizar"
O KPI "Vendas Hoje" deve aumentar
```

---

## 📱 Passo 9: Ajustes Finais

### 9.1 Responsividade
1. Teste em diferentes tamanhos de tela
2. Ajuste o layout para mobile se necessário
3. Procure por **"Page Settings"** > **"Responsive**

### 9.2 Ordenação e Filtros
1. Nos gráficos e tabelas, adicione:
   - Ordenação padrão
   - Filtros (opcional)
   - Paginação

### 9.3 Refresh Automático (Opcional)
1. Vá para **"Page Settings"**
2. Procure por **"Refresh"** ou **"Auto-Refresh"**
3. Configure para atualizar a cada 30 segundos (depende da sua necessidade)

---

## ✅ Checklist Final

- [ ] Página 1 criada com nome "HOME"
- [ ] 4 Cards de KPI adicionados
- [ ] 3 Gráficos criados e testados
- [ ] 2 Regiões de alertas com dados
- [ ] Layout organizado e responsivo
- [ ] Botão "Atualizar" funciona
- [ ] Todos os números mostram dados corretos
- [ ] Página salva
- [ ] Testes passaram

---

## 🎯 Resultado Esperado

Quando pronto, sua página HOME terá este aspecto:

```
┌─────────────────────────────────────────────────────┐
│ HOME - Sistema de Gestão de Mercado                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Vendas Hoje]  [Faturamento Mês] [Em Falta] [Clientes]
│    R$ 1.250,00      R$ 15.680,00       5        127
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Gráfico Vendas]  [Top 5 Produtos] [Pagamentos]   │
│  (Linha 7 dias)      (Barras)          (Pizza)     │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ⚠️ Produtos em Falta:                              │
│  ┌────────────────────────────────────────────┐   │
│  │ Produto       | Qtd. | Mínimo             │   │
│  │ Água 1.5L    | 5    | 50                 │   │
│  │ Feijão 1kg   | 8    | 20                 │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📦 Compras Pendentes:                              │
│  ┌────────────────────────────────────────────┐   │
│  │ Fornecedor    | Valor     | Data           │   │
│  │ Distribuidora | R$ 5.000  | 13/07/2026    │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  [↻ Atualizar Dashboard]                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Próximos Passos

Após criar a HOME, você criará:
1. ✅ **HOME** (Página 1) ← VOCÊ ESTÁ AQUI
2. ⏳ **Página 10:** Listar Produtos
3. ⏳ **Página 11:** Criar/Editar Produto
4. ⏳ **Página 20:** PDV (Carrinho)
5. ⏳ **Página 21:** PDV (Confirmação)
6. ⏳ **Página 30:** Histórico de Vendas
7. ⏳ **Página 40:** Estoque (Movimentações)
8. ⏳ **Página 50:** Compras

---

## 💡 Dicas Importantes

### Dica 1: Dados de Teste
Se os KPIs mostrarem 0, insira dados de teste em SQL:
```sql
INSERT INTO VENDAS (cliente_id, valor_total, valor_final, forma_pagamento, status)
VALUES (1, 100, 100, 'DINHEIRO', 'CONCLUIDA');
COMMIT;
```

### Dica 2: Salvar Frequentemente
Use Ctrl+S para salvar a cada mudança importante.

### Dica 3: Preview Mobile
Clique em **"View"** > **"Device Preview"** para ver em mobile.

### Dica 4: Melhorar Performance
Se os gráficos forem lentos, adicione um filtro de data:
```sql
WHERE data_venda >= TRUNC(SYSDATE) - 30
```

---

## 🎓 Recursos Úteis

- [APEX Interactive Grid Docs](https://docs.oracle.com/en/database/oracle/apex/21.1/htmdb/using-interactive-grids.html)
- [APEX Charts](https://docs.oracle.com/en/database/oracle/apex/21.1/htmdb/using-charts.html)
- [APEX Page Designer](https://docs.oracle.com/en/database/oracle/apex/21.1/htmdb/using-page-designer.html)

---

**Versão:** 1.0  
**Data:** Julho 2026  
**Status:** Pronto para implementar

Bom desenvolvimento! 🚀
