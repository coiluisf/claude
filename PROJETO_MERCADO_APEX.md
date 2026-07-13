# 🏪 Sistema de Gestão de Mercado - Oracle APEX

**Versão:** 1.0  
**Data:** Julho 2026  
**Ambiente:** Oracle Cloud Free Tier + Oracle APEX

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Requisitos Técnicos](#requisitos-técnicos)
3. [Arquitetura do Sistema](#arquitetura-do-sistema)
4. [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
5. [Módulos da Aplicação](#módulos-da-aplicação)
6. [Funcionalidades Principais](#funcionalidades-principais)
7. [Fluxos de Trabalho](#fluxos-de-trabalho)
8. [Setup e Instalação](#setup-e-instalação)

---

## 🎯 Visão Geral

O **Sistema de Gestão de Mercado** é uma solução web completa para gerenciar operações de um mercado/supermercado de pequeno a médio porte. O sistema foi desenvolvido em **Oracle APEX** e oferece funcionalidades robustas para:

- ✅ Gerenciamento de Produtos e Estoque
- ✅ Vendas com PDV (Ponto de Venda)
- ✅ Gestão de Clientes
- ✅ Controle de Compras e Fornecedores
- ✅ Movimentação de Estoque
- ✅ Relatórios e Dashboards

### Público-Alvo
- Pequenos e médios mercados
- Lojas de alimentos
- Comércios em geral

### Benefícios
- Controle em tempo real do estoque
- Histórico de vendas
- Relatórios gerenciais
- Interface web amigável
- Baixo custo de infraestrutura (Free Tier Oracle Cloud)

---

## 💻 Requisitos Técnicos

### Infrastructure
- **Banco de Dados:** Oracle Autonomous Database (Free Tier)
- **Plataforma:** Oracle APEX 23.1+
- **Navegador:** Chrome, Firefox, Safari, Edge (versões recentes)
- **Conexão:** Internet (acesso ao Oracle Cloud)

### Contas Necessárias
- Conta Oracle Cloud (gratuita)
- Email válido para confirmação

### Softwares Opcionais
- SQL Developer (para desenvolvimento avançado)
- SQL Developer Web (nativo no Oracle Cloud)

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────┐
│         APLICAÇÃO ORACLE APEX               │
│  (Interface Web - Páginas e Componentes)    │
└─────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────┐
│      CAMADA DE LÓGICA (PL/SQL)              │
│  (Procedures, Triggers, Functions)          │
└─────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────┐
│      BANCO DE DADOS (Tabelas, Views)        │
│  (Oracle Autonomous Database)               │
└─────────────────────────────────────────────┘
```

### Tecnologias Utilizadas
- **Frontend:** APEX UI Components (Interactive Grids, Forms, Charts)
- **Backend:** PL/SQL (Procedures, Triggers)
- **Database:** Oracle SQL
- **Servidor Web:** APEX Application Server
- **Autenticação:** APEX Workspace

---

## 📊 Estrutura do Banco de Dados

### Tabelas Principais

#### 1. **CATEGORIAS**
Classifica os produtos por tipo.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| categoria_id | NUMBER (PK) | ID único |
| nome | VARCHAR2(100) | Nome da categoria |
| descricao | VARCHAR2(500) | Descrição |
| ativa | CHAR(1) | Status (S/N) |
| criada_em | TIMESTAMP | Data de criação |

---

#### 2. **PRODUTOS**
Catálogo de produtos do mercado.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| produto_id | NUMBER (PK) | ID único |
| categoria_id | NUMBER (FK) | Categoria |
| nome | VARCHAR2(150) | Nome produto |
| descricao | VARCHAR2(500) | Descrição |
| preco_custo | NUMBER(10,2) | Custo de compra |
| preco_venda | NUMBER(10,2) | Preço de venda |
| quantidade | NUMBER(10,2) | Estoque atual |
| estoque_minimo | NUMBER(10,2) | Quantidade mínima |
| sku | VARCHAR2(50) | Código único |
| ativo | CHAR(1) | Status |

---

#### 3. **CLIENTES**
Base de clientes do mercado.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| cliente_id | NUMBER (PK) | ID único |
| nome | VARCHAR2(150) | Nome cliente |
| cpf | VARCHAR2(14) | CPF (único) |
| email | VARCHAR2(100) | Email |
| telefone | VARCHAR2(20) | Telefone |
| endereco | VARCHAR2(300) | Endereço |
| cidade | VARCHAR2(100) | Cidade |
| estado | VARCHAR2(2) | UF |
| tipo | VARCHAR2(20) | FISICO/JURIDICO |
| ativo | CHAR(1) | Status |

---

#### 4. **VENDAS**
Registro de todas as vendas realizadas.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| venda_id | NUMBER (PK) | ID único |
| cliente_id | NUMBER (FK) | Cliente |
| data_venda | DATE | Data da venda |
| valor_total | NUMBER(12,2) | Total bruto |
| desconto | NUMBER(12,2) | Desconto |
| valor_final | NUMBER(12,2) | Total final |
| forma_pagamento | VARCHAR2(50) | Método pagamento |
| status | VARCHAR2(20) | CONCLUIDA/CANCELADA |
| observacoes | VARCHAR2(500) | Notas |

---

#### 5. **ITENS_VENDA**
Itens contidos em cada venda.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| item_venda_id | NUMBER (PK) | ID único |
| venda_id | NUMBER (FK) | Venda |
| produto_id | NUMBER (FK) | Produto |
| quantidade | NUMBER(10,2) | Qtd vendida |
| preco_unitario | NUMBER(10,2) | Preço unitário |
| desconto_item | NUMBER(12,2) | Desconto |
| subtotal | NUMBER(12,2) | Total item |

---

#### 6. **MOVIMENTACOES_ESTOQUE**
Histórico de movimentações de estoque.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| movimentacao_id | NUMBER (PK) | ID único |
| produto_id | NUMBER (FK) | Produto |
| tipo_movimento | VARCHAR2(20) | ENTRADA/SAIDA |
| quantidade | NUMBER(10,2) | Quantidade |
| motivo | VARCHAR2(200) | Motivo |
| referencia_id | NUMBER | ID da venda/compra |
| referencia_tipo | VARCHAR2(50) | VENDA/COMPRA |

---

#### 7. **FORNECEDORES**
Base de fornecedores.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| fornecedor_id | NUMBER (PK) | ID único |
| nome | VARCHAR2(150) | Nome fornecedor |
| cnpj | VARCHAR2(18) | CNPJ |
| email | VARCHAR2(100) | Email |
| telefone | VARCHAR2(20) | Telefone |
| ativo | CHAR(1) | Status |

---

#### 8. **COMPRAS** e **ITENS_COMPRA**
Registro de compras junto aos fornecedores.

---

### Views Principais

#### `PRODUTOS_COM_ALERTA`
Produtos com status de estoque (NORMAL, BAIXO, CRÍTICO).

#### `VENDAS_DIARIAS`
Resumo de vendas por dia.

#### `PRODUTOS_MAIS_VENDIDOS`
Ranking dos 10 produtos mais vendidos.

#### `SALDO_CLIENTES`
Total gasto por cliente.

---

## 📱 Módulos da Aplicação

A aplicação APEX será dividida em **5 módulos principais**:

### 1. **HOME (Página 1)**
- Dashboard executivo
- KPIs principais
- Gráficos de vendas
- Status do estoque

### 2. **PRODUTOS (Páginas 10-11)**
- Lista de produtos
- Formulário de cadastro/edição
- Importação de produtos
- Controle de categorias

### 3. **PDV - PONTO DE VENDA (Páginas 20-21)**
- Interface de venda rápida
- Carrinho de compras
- Cálculo automático
- Formas de pagamento
- Confirmação de venda

### 4. **VENDAS (Página 30)**
- Histórico de vendas
- Filtros e buscas
- Devolução de vendas
- Relatórios

### 5. **ESTOQUE (Página 40)**
- Movimentação de estoque
- Ajustes manuais
- Alertas de estoque baixo
- Histórico completo

### 6. **COMPRAS (Página 50)**
- Pedidos de compra
- Gestão de fornecedores
- Recebimento
- Histórico

---

## 🎯 Funcionalidades Principais

### 1. Gestão de Produtos
```
- ✅ Cadastrar novo produto
- ✅ Editar informações do produto
- ✅ Definir preço de custo e venda
- ✅ Configurar estoque mínimo
- ✅ Ativar/desativar produtos
- ✅ Importar planilha de produtos
- ✅ Gerar relatório de produtos
```

### 2. Ponto de Venda (PDV)
```
- ✅ Buscar produto por nome ou código
- ✅ Adicionar itens ao carrinho
- ✅ Remover ou alterar quantidade
- ✅ Calcular total automaticamente
- ✅ Aplicar desconto
- ✅ Selecionar forma de pagamento
- ✅ Emitir nota de venda (impressão)
- ✅ Finalizar venda
```

### 3. Gestão de Estoque
```
- ✅ Visualizar quantidade em tempo real
- ✅ Receber mercadoria (entrada)
- ✅ Fazer ajustes manuais
- ✅ Ver histórico de movimentações
- ✅ Alertas de estoque baixo
- ✅ Relatório de produtos críticos
```

### 4. Gestão de Clientes
```
- ✅ Cadastrar cliente
- ✅ Editar informações
- ✅ Histórico de compras
- ✅ Saldo a pagar (crediário)
- ✅ Ativar/desativar cliente
```

### 5. Relatórios e Dashboards
```
- ✅ Dashboard de vendas diárias
- ✅ Produtos mais vendidos
- ✅ Estoque crítico
- ✅ Faturamento por período
- ✅ Desempenho por categoria
- ✅ Análise de clientes
```

---

## 🔄 Fluxos de Trabalho

### Fluxo 1: Venda Simples (PDV)

```
1. Acessar módulo PDV
   ↓
2. Buscar/Escanear produto
   ↓
3. Adicionar ao carrinho
   ↓
4. Repetir para próximos itens
   ↓
5. Revisar carrinho
   ↓
6. Aplicar desconto (se houver)
   ↓
7. Selecionar forma de pagamento
   ↓
8. Confirmar venda
   ↓
9. Imprimir cupom
   ↓
10. Venda registrada com sucesso ✅
```

### Fluxo 2: Recebimento de Compra

```
1. Criar pedido de compra
   ↓
2. Selecionar fornecedor
   ↓
3. Adicionar produtos
   ↓
4. Informar quantidade
   ↓
5. Confirmar pedido
   ↓
6. Quando mercadoria chegar...
   ↓
7. Marcar como recebida
   ↓
8. Estoque atualizado automaticamente ✅
```

### Fluxo 3: Ajuste de Estoque

```
1. Acessar movimentação de estoque
   ↓
2. Selecionar produto
   ↓
3. Escolher tipo (Entrada/Saída/Ajuste)
   ↓
4. Informar quantidade
   ↓
5. Informar motivo
   ↓
6. Confirmar
   ↓
7. Movimentação registrada ✅
```

---

## 🚀 Setup e Instalação

### Pré-requisitos
- Conta Oracle Cloud (gratuita)
- Acesso ao Console Oracle Cloud
- Email válido

### Passo 1: Criar Conta Oracle Cloud
```
1. Acesse: https://www.oracle.com/cloud/free/
2. Clique "Criar Conta Gratuita"
3. Preencha informações pessoais
4. Confirme email
5. Você está pronto para usar o Free Tier
```

### Passo 2: Provisionar Banco de Dados
```
1. Console Oracle Cloud
2. Menu → Database → Autonomous Database
3. Create Autonomous Database
4. Workload Type: Transaction Processing
5. Deployment: Shared Infrastructure
6. Database Name: MERCADO_DB
7. License: Always Free
8. Clique "Create"
9. Aguarde 2-3 minutos
```

### Passo 3: Executar Script SQL
```
1. No Oracle Cloud Console, clique em MERCADO_DB
2. Clique "Database Actions"
3. Login com ADMIN
4. Abra "SQL"
5. Cole o conteúdo do arquivo: 01_CREATE_DATABASE_SCHEMA.sql
6. Execute (Ctrl+Enter)
7. Aguarde mensagem de sucesso
```

### Passo 4: Criar Workspace APEX
```
1. Console Oracle Cloud → MERCADO_DB
2. Clique "Database Actions"
3. Você será levado ao APEX
4. Clique "Manage Workspaces"
5. Create Workspace
6. Workspace: MERCADO_FAMILIA
7. Username: APEX_DEVELOPER
8. Clique "Create Workspace"
```

### Passo 5: Criar Aplicação
```
1. Logout da workspace INTERNAL
2. Login em MERCADO_FAMILIA com APEX_DEVELOPER
3. App Builder → Create → From Scratch
4. Name: Sistema de Gestão de Mercado
5. Schema: APEX_DEVELOPER
6. Clique "Create Application"
```

### Passo 6: Desenvolvendo as Páginas
Este é o próximo passo após o setup básico. Você receberá documentação específica para cada página.

---

## 📚 Documentação Técnica

### Scripts SQL Fornecidos
- `01_CREATE_DATABASE_SCHEMA.sql` - Cria toda a estrutura do banco

### Próximos Arquivos
- `GUIA_SETUP_PASSO_A_PASSO.md` - Instruções detalhadas
- `02_CREATE_APEX_PAGES.sql` - Criação das páginas APEX
- `03_CREATE_APEX_ITEMS.sql` - Componentes APEX
- `RELATORIOS_SQL.sql` - Queries para relatórios

---

## 🔐 Segurança

### Boas Práticas Implementadas
- ✅ Senhas fortes (obrigatórias)
- ✅ Validação de entrada
- ✅ Constraints no banco
- ✅ Auditoria de transações
- ✅ Controle de acesso por workspace

### Recomendações Adicionais
1. Faça backup regular do banco
2. Mantenha as senhas seguras
3. Use HTTPS em produção
4. Implemente logs de auditoria
5. Faça testes antes de usar em produção

---

## 📞 Suporte e Troubleshooting

### Problema: Workspace não criado
**Solução:** Verifique se executou corretamente o Passo 4 do setup.

### Problema: Tabelas não aparecem em APEX
**Solução:** Execute o script `01_CREATE_DATABASE_SCHEMA.sql` novamente e verifique a schema.

### Problema: Banco demora para provisionar
**Solução:** Free Tier pode levar até 10 minutos. Recarregue a página.

---

## 📈 Próximos Passos

1. ✅ Completar setup técnico (este documento)
2. ⏳ Criar páginas APEX (HOME, Produtos, PDV, etc)
3. ⏳ Configurar componentes visuais
4. ⏳ Testar fluxos de trabalho
5. ⏳ Treinamento de usuários
6. ⏳ Deploy em produção

---

## 📝 Histórico de Versões

| Versão | Data | Alterações |
|--------|------|-----------|
| 1.0 | Jul/2026 | Versão inicial |

---

## 📧 Contato

**Desenvolvedor:** Claude Code  
**Email:** coiluisf@gmail.com  
**Projeto:** Sistema de Gestão de Mercado - APEX

---

**Status:** ✅ Pronto para Setup  
**Última Atualização:** 13 de Julho de 2026
