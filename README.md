# 🏪 Sistema de Gestão de Mercado - Oracle APEX

**Uma solução completa em Oracle APEX para gerenciar mercados e pequenos supermercados.**

[![Status](https://img.shields.io/badge/Status-Setup%20Ready-brightgreen)]()
[![Oracle APEX](https://img.shields.io/badge/Oracle%20APEX-23.1%2B-blue)]()
[![Oracle Cloud](https://img.shields.io/badge/Oracle%20Cloud-Free%20Tier-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

---

## 🎯 O que é?

Um sistema web moderno e intuitivo para gerenciar operações de um mercado ou pequeno supermercado, incluindo:

- 📊 **Dashboard executivo** com KPIs
- 🏷️ **Gestão de produtos** e categorias
- 💰 **PDV inteligente** (Ponto de Venda)
- 📦 **Controle de estoque** em tempo real
- 👥 **Gestão de clientes** e crediário
- 🛒 **Histórico de vendas** completo
- 📞 **Compras e fornecedores**
- 📈 **Relatórios e análises**

---

## ⚡ Quick Start

### 1️⃣ Setup (30 minutos)

```bash
# Siga este guia passo-a-passo (em português):
📖 GUIA_SETUP_PASSO_A_PASSO.md
```

### 2️⃣ Executar Script SQL

```sql
-- No SQL Developer Web, execute:
01_CREATE_DATABASE_SCHEMA.sql
```

### 3️⃣ Você está pronto! 🎉

Sua aplicação APEX estará pronta com:
- ✅ 8 tabelas criadas
- ✅ 10 triggers automáticos
- ✅ 5 views analíticas
- ✅ Dados de exemplo
- ✅ Tudo funcionando

---

## 📁 Arquivos Deste Projeto

| Arquivo | Descrição | Leia Primeiro? |
|---------|-----------|----------------|
| **README.md** | Este arquivo | ✅ Aqui |
| **GUIA_SETUP_PASSO_A_PASSO.md** | Setup completo em português | ✅ Segundo |
| **PROJETO_MERCADO_APEX.md** | Documentação técnica do projeto | ⏳ Depois |
| **01_CREATE_DATABASE_SCHEMA.sql** | Script para criar banco | ✅ Terceiro |

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────┐
│   APLICAÇÃO ORACLE APEX WEB     │
│  (Interface dos usuários)        │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│    LÓGICA PL/SQL               │
│  (Procedures, Triggers)         │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│   ORACLE DATABASE FREE TIER     │
│  (Tabelas, Views, Sequences)    │
└─────────────────────────────────┘
```

### Tecnologias
- **Frontend:** Oracle APEX UI Components
- **Backend:** PL/SQL (Procedures, Triggers)
- **Banco:** Oracle Autonomous Database
- **Hospedagem:** Oracle Cloud (Free Tier)
- **Acesso:** Web browser (https)

---

## 📊 Módulos da Aplicação

Após o setup, a aplicação terá os seguintes módulos:

### 🏠 HOME (Página 1)
- Dashboard com vendas do dia
- KPIs principais
- Alertas de estoque
- Gráficos de tendências

### 📦 PRODUTOS (Páginas 10-11)
- Listar todos os produtos
- Cadastrar novo produto
- Editar informações
- Importar produtos em Excel

### 💳 PDV - PONTO DE VENDA (Páginas 20-21)
- Interface de venda rápida
- Buscar produtos
- Carrinho de compras
- Calcular totais
- Várias formas de pagamento
- Imprimir nota fiscal

### 📋 VENDAS (Página 30)
- Ver histórico de vendas
- Buscar e filtrar
- Devolução
- Relatórios

### 📦 ESTOQUE (Página 40)
- Ver quantidade em tempo real
- Fazer ajustes
- Receber mercadoria
- Ver movimentações
- Alertas de estoque baixo

### 🤝 COMPRAS (Página 50)
- Gestão de fornecedores
- Criar pedidos
- Receber compras
- Histórico

---

## 🚀 Como Começar

### Pré-requisitos
- ✅ Conta de email válida
- ✅ Acesso à internet
- ✅ Navegador web moderno
- ✅ **NÃO precisa instalar nada no seu computador!**

### Passo 1: Criar Conta Oracle Cloud
```
Acesse: https://www.oracle.com/cloud/free/
Clique: "Criar Conta Gratuita"
⏱️ Tempo: 5-10 minutos
```

### Passo 2: Provisionar Banco de Dados
```
Oracle Cloud Console
→ Database → Autonomous Database
→ Create Autonomous Database
⏱️ Tempo: 5 minutos (mais 2-3 para provisionar)
```

### Passo 3: Executar Script SQL
```
Abra: SQL Developer Web
Cole: 01_CREATE_DATABASE_SCHEMA.sql
Clique: RUN
⏱️ Tempo: 2-3 minutos
```

### Passo 4: Criar Workspace APEX
```
Oracle Cloud Console
→ APEX → Manage Workspaces
→ Create Workspace
⏱️ Tempo: 5 minutos
```

### Passo 5: Pronto! 🎉
```
Login em APEX
Start Builder
Desenvolva suas páginas!
```

**Tempo Total:** ~30-45 minutos

---

## 📖 Documentação Completa

### Para Começar
1. **GUIA_SETUP_PASSO_A_PASSO.md** - Instruções detalhadas do setup
2. **PROJETO_MERCADO_APEX.md** - Visão geral do projeto

### Para Desenvolver (Próximos)
- Documentação de cada página APEX
- Queries SQL para relatórios
- Código de procedures

### Referência
- [Oracle APEX Docs](https://docs.oracle.com/en/database/oracle/apex/)
- [Oracle Cloud Docs](https://docs.oracle.com/en-us/iaas/Content/home.htm)
- [SQL Developer Web](https://docs.oracle.com/en/database/oracle/sql-developer-web/)

---

## 💾 Estrutura do Banco de Dados

### Tabelas Principais
```
CATEGORIAS          ← Categorias de produtos
├─ PRODUTOS         ← Produtos (vinculados a categorias)
│  ├─ ITENS_VENDA   ← Itens de cada venda
│  ├─ ITENS_COMPRA  ← Itens de cada compra
│  └─ MOVIMENTAÇÕES_ESTOQUE ← Histórico de estoque
│
CLIENTES            ← Base de clientes
└─ VENDAS           ← Vendas (vinculadas a clientes)
   └─ ITENS_VENDA   (vinculado acima)

FORNECEDORES        ← Fornecedores
└─ COMPRAS          ← Pedidos de compra
   └─ ITENS_COMPRA  (vinculado acima)
```

### Automatizações
- ✅ Auto-incremento de IDs (via Sequences)
- ✅ Atualização de estoque automática
- ✅ Registro de movimentações
- ✅ Cálculos automáticos

### Views Analíticas
- `PRODUTOS_COM_ALERTA` - Estoque crítico
- `VENDAS_DIARIAS` - Vendas por dia
- `PRODUTOS_MAIS_VENDIDOS` - Top 10 produtos
- `SALDO_CLIENTES` - Total gasto por cliente

---

## ✅ Checklist de Configuração

Antes de usar, certifique-se de:

- [ ] Conta Oracle Cloud criada
- [ ] Banco MERCADO_DB provisionado
- [ ] Script SQL 01_CREATE_DATABASE_SCHEMA.sql executado
- [ ] Workspace MERCADO_FAMILIA criado
- [ ] Usuário APEX_DEVELOPER criado
- [ ] Login em MERCADO_FAMILIA funcionando
- [ ] Aplicação criada em APEX
- [ ] Tabelas visíveis em SQL Workshop
- [ ] Query de teste retornou dados

---

## 🔐 Segurança

### Implementado
- ✅ Senhas fortes (obrigatórias)
- ✅ Validação de entrada
- ✅ Constraints no banco
- ✅ Auditoria de transações
- ✅ Controle de acesso por workspace

### Recomendações
- Mude as senhas padrão regularmente
- Faça backup do banco regularmente
- Use HTTPS em produção
- Implemente logs de auditoria
- Teste as permissões de acesso

---

## 🆘 Troubleshooting Rápido

### "Workspace não existe"
→ Volte ao Passo 7 do guia de setup

### "Tabelas não aparecem"
→ Execute: `SELECT * FROM CATEGORIAS;` em SQL
→ Se erro, execute o script SQL novamente

### "Erro ao fazer login"
→ Verifique workspace, usuário e senha
→ Limpe cache do navegador

### "Banco demora para provisionar"
→ Normal! Pode levar até 10 minutos em Free Tier
→ Recarregue a página a cada 2 minutos

### Mais problemas?
→ Veja seção "Troubleshooting" do GUIA_SETUP_PASSO_A_PASSO.md

---

## 📞 Contato e Suporte

**Desenvolvedor:** Claude Code  
**Email:** coiluisf@gmail.com  
**Projeto:** Sistema de Gestão de Mercado - APEX  
**Versão:** 1.0  
**Data:** Julho 2026

---

## 📈 Próximas Fases

### Fase 1: ✅ Setup Técnico
- [x] Estrutura de banco de dados
- [x] Dados de exemplo
- [x] Workspace APEX

### Fase 2: ⏳ Desenvolvimento APEX
- [ ] Criar páginas APEX
- [ ] Componentes visuais
- [ ] Integração com banco

### Fase 3: ⏳ Testes e Refinamento
- [ ] Testes de fluxo
- [ ] Performance
- [ ] Ajustes de UX

### Fase 4: ⏳ Deploy e Treinamento
- [ ] Deploy em produção
- [ ] Backup e recuperação
- [ ] Treinamento de usuários

---

## 📜 License

MIT License - Você é livre para usar, modificar e distribuir este projeto.

---

## 🎉 Começando

**Leia agora:** [`GUIA_SETUP_PASSO_A_PASSO.md`](./GUIA_SETUP_PASSO_A_PASSO.md)

Tempo estimado: **30-45 minutos** para o setup completo.

---

**Versionamento:** 1.0  
**Status:** ✅ Pronto para Setup  
**Última atualização:** 13 de Julho de 2026

Boa sorte! 🚀
