# 🚀 Guia Passo-a-Passo: Setup Oracle APEX para Sistema de Mercado

**Tempo Estimado:** 30-45 minutos  
**Nível:** Iniciante  
**Requisitos:** Conta de email válida

---

## 📋 Checklist de Pré-requisitos

- [ ] Você tem acesso à internet
- [ ] Tem uma conta de email válida (pessoal ou corporativa)
- [ ] Tem acesso a um navegador web moderno (Chrome, Firefox, Edge)
- [ ] Tem um computador com capacidade para acessar Oracle Cloud

---

## PASSO 1: Criar Conta Oracle Cloud (Se não tiver)

### 1.1 Acessar o site

1. Abra seu navegador
2. Acesse: **https://www.oracle.com/cloud/free/**
3. Você verá a página de Free Tier do Oracle Cloud

### 1.2 Clicar em "Criar Conta"

1. Procure pelo botão azul **"Criar Conta Gratuita"** ou **"Start for Free"**
2. Clique nele
3. Você será redirecionado para o formulário de inscrição

### 1.3 Preencher Dados Pessoais

1. **Country:** Brasil
2. **Email:** Seu email pessoal ou corporativo
3. **Name:** Seu nome completo
4. **Company Name:** Nome da sua empresa (pode ser seu nome também)
5. **Address:** Seu endereço
6. **City:** Sua cidade
7. **State:** UF (ex: SP)
8. **ZIP Code:** CEP
9. **Phone:** Seu telefone com código do país (+55)

✅ **Dica:** Preencha tudo com dados reais. Oracle pode solicitar verificação.

### 1.4 Dados de Pagamento

1. **Método:** Cartão de crédito (Visa, Mastercard, Elo)
2. **Número do Cartão:** Seu número de cartão
3. **Data Expiração:** Mês/Ano
4. **CVV:** 3 dígitos atrás do cartão

⚠️ **Importante:** No Free Tier, seu cartão NÃO será cobrado. Oracle apenas verifica que é válido.

### 1.5 Confirmar Email

1. Você receberá um email da Oracle
2. Clique no link de confirmação
3. Aguarde a confirmação ser processada (pode levar alguns minutos)

✅ **Pronto!** Sua conta Oracle Cloud está criada.

---

## PASSO 2: Provisionar Oracle Database Free

### 2.1 Acessar o Console

1. Faça login em: **https://cloud.oracle.com**
2. Use suas credenciais criadas no Passo 1
3. Você verá o Oracle Cloud Console

### 2.2 Navegar até Autonomous Database

1. Clique no **Menu ≡** (três linhas) no canto superior esquerdo
2. Selecione **Database**
3. Clique em **Autonomous Database**

### 2.3 Criar Database

1. Clique no botão azul **"Create Autonomous Database"**
2. Uma página de formulário abrirá

### 2.4 Configurar o Banco de Dados

**Compartment (Se perguntado):**
- Selecione o compartment padrão

**Display Name:**
```
MERCADO_DB
```

**Database Name:**
```
MERCADODB
```

**Workload Type:**
- Selecione: ✅ **Transaction Processing**
  (Não "Data Warehouse")

**Deployment Type:**
- Selecione: ✅ **Shared Infrastructure**
  (Para usar o Free Tier)

**Database Version:**
- Deixe a versão mais recente selecionada (ex: 23c)

**ADMIN Password:**
```
SenhaSegura123!@
```

⚠️ **Importante:** Guarde bem essa senha! Você precisará dela.

**License Type:**
- Selecione: ✅ **Always Free**
  (Essencial para Free Tier)

**Storage:**
- Deixe como padrão (geralmente 20GB)

### 2.5 Criar Database

1. Clique no botão verde **"Create Autonomous Database"**
2. Você verá uma página de status: "Provisioning"
3. Aguarde 2-3 minutos enquanto o banco é criado

✅ **Status:** Quando estiver verde escrito "AVAILABLE", prossiga.

---

## PASSO 3: Acessar SQL Developer Web

### 3.1 Abrir o Database

1. No Oracle Cloud Console, você verá seu banco "MERCADO_DB"
2. Clique no nome do banco para abrir seus detalhes

### 3.2 Acessar SQL

1. Procure pelo botão **"Database Actions"** (azul)
2. Ou procure por **"SQL"** ou **"SQL Developer Web"**
3. Clique nele
4. Uma aba nova abrirá

### 3.3 Fazer Login no SQL Developer Web

1. **Username:** `ADMIN`
2. **Password:** A senha que você criou no Passo 2 (SenhaSegura123!@)
3. Clique **"Sign In"**

✅ **Pronto!** Você está agora em SQL Developer Web. Você verá um editor SQL vazio.

---

## PASSO 4: Executar Script de Criação do Schema

### 4.1 Abrir uma Nova Aba SQL

1. Você pode estar em uma aba padrão
2. Se necessário, clique em **"SQL"** na barra de menus
3. Ou clique no ícone de **"+"** para nova aba

### 4.2 Copiar o Script SQL

1. Abra o arquivo: **`01_CREATE_DATABASE_SCHEMA.sql`**
2. Selecione TODO o conteúdo (Ctrl+A)
3. Copie (Ctrl+C)

### 4.3 Colar no SQL Developer Web

1. Clique na área de edição do SQL Developer Web
2. Cole o script (Ctrl+V)
3. Você verá o script completo na tela

### 4.4 Executar o Script

**Opção A - Executar Tudo:**
1. Pressione **Ctrl+Enter**
   OU
2. Clique no botão ▶ (Play/Run)

**Opção B - Executar por Partes:**
1. Selecione um comando SQL
2. Pressione Ctrl+Enter

### 4.5 Aguardar Execução

1. Você verá mensagens na aba "Results" abaixo
2. Procure por: `"Sistema de Gestão de Mercado - Base de dados criada com sucesso!"`
3. Se ver ERROS, copie a mensagem de erro e revise o script

✅ **Sucesso:** Você verá mensagens como:
```
Table CATEGORIAS created.
Table PRODUTOS created.
...
Sistema de Gestão de Mercado - Base de dados criada com sucesso!
```

---

## PASSO 5: Criar Workspace APEX

### 5.1 Acessar APEX

**Opção A - Via Console:**
1. Volte ao Oracle Cloud Console
2. Clique em seu banco MERCADO_DB
3. Clique em **"Database Actions"** novamente
4. Procure pela opção **"Manage Workspaces"** ou vá direto para APEX

**Opção B - URL Direta:**
1. A URL será algo como: `https://[your-instance].adb.us-xxxx-1.oraclecloud.com/ords/apex`

### 5.2 Login Inicial no APEX

1. **Workspace:** `INTERNAL`
2. **Username:** `ADMIN`
3. **Password:** A senha que você criou no Passo 2
4. Clique **"Sign In"**

✅ **Você está agora no APEX INTERNAL workspace.**

### 5.3 Acessar Manage Workspaces

1. Procure pelo botão/menu **"Manage Workspaces"**
2. Ou use o painel de administração
3. Clique em **"Create Workspace"**

### 5.4 Criar Novo Workspace

**Workspace Name:**
```
MERCADO_FAMILIA
```

**Workspace Username:**
```
APEX_DEVELOPER
```

**Workspace Password:**
```
SenhaAPEX123!@
```

⚠️ **Importante:** Use uma senha forte com números e símbolos.

**Re-enter Password:**
```
SenhaAPEX123!@
```

Workspace Schema: (deixe como padrão)

### 5.5 Criar Workspace

1. Clique no botão **"Create Workspace"**
2. Aguarde a confirmação

✅ **Workspace MERCADO_FAMILIA criado com sucesso!**

---

## PASSO 6: Login no Novo Workspace

### 6.1 Logout do INTERNAL

1. Procure pelo seu nome de usuário no canto superior direito
2. Clique
3. Selecione **"Sign Out"** ou **"Logout"**

### 6.2 Voltar ao Login APEX

1. Você será levado de volta à página de login do APEX
2. Procure por uma opção para **"Change Workspace"**
3. Ou simplesmente limpe o campo "Workspace"

### 6.3 Fazer Login no Novo Workspace

1. **Workspace:** `MERCADO_FAMILIA`
2. **Username:** `APEX_DEVELOPER`
3. **Password:** `SenhaAPEX123!@` (a que você criou)
4. Clique **"Sign In"**

✅ **Você está agora no workspace MERCADO_FAMILIA!**

---

## PASSO 7: Criar a Aplicação APEX

### 7.1 Acessar App Builder

1. Você verá o dashboard do workspace
2. Procure pelo botão/menu **"App Builder"**
3. Clique nele

### 7.2 Criar Aplicação

1. Clique no botão azul **"Create"**
2. Você verá opções de templates

### 7.3 Escolher "From Scratch"

1. Selecione **"From Scratch"**
   (Não use templates pré-prontos por agora)

### 7.4 Configurar Aplicação

**Name:**
```
Sistema de Gestão de Mercado
```

**Schema:**
- Selecione: `APEX_DEVELOPER`
  (ou o schema padrão)

**Other Options:** (deixe como padrão)

### 7.5 Criar Aplicação

1. Clique no botão **"Create Application"**
2. Aguarde alguns segundos

✅ **Sua aplicação foi criada!** 🎉

Você verá a página da aplicação com opções para adicionar páginas.

---

## PASSO 8: Verificar Conexão com Banco de Dados

### 8.1 Acessar SQL Workshop

1. Procure pelo menu/aba **"SQL Workshop"**
2. Ou clique em seu nome de usuário → **"SQL Workshop"**

### 8.2 Acessar SQL Commands

1. Selecione **"SQL Commands"**

### 8.3 Executar Query de Teste

1. Na área de edição, digite:
```sql
SELECT COUNT(*) as TOTAL_PRODUTOS FROM PRODUTOS;
```

2. Clique **"Run"** (ou Ctrl+Enter)

### 8.4 Verificar Resultado

Se você ver:
```
TOTAL_PRODUTOS
10
```

✅ **Perfeito! Banco de dados conectado e funcionando!**

Se ver erro "Table not found", volte ao Passo 4 e revise a execução do script SQL.

---

## PASSO 9: Estrutura Após Setup

```
ORACLE CLOUD
├── Database: MERCADO_DB
│   ├── Admin User: ADMIN (criou o banco)
│   ├── APEX User: APEX_DEVELOPER
│   └── Schema com:
│       ├── 8 Tabelas (CATEGORIAS, PRODUTOS, etc)
│       ├── 9 Sequences
│       ├── 10 Triggers
│       ├── 5 Views
│       └── 1 Procedure
│
└── APEX Workspace: MERCADO_FAMILIA
    └── Application: Sistema de Gestão de Mercado
        └── Estrutura pronta para desenvolver!
```

---

## ✅ Checklist Final de Verificação

Antes de prosseguir, verifique:

- [ ] Conta Oracle Cloud criada
- [ ] Banco de dados MERCADO_DB provisionado
- [ ] Script SQL 01_CREATE_DATABASE_SCHEMA.sql executado
- [ ] Workspace MERCADO_FAMILIA criado
- [ ] Usuário APEX_DEVELOPER criado
- [ ] Login bem-sucedido em MERCADO_FAMILIA
- [ ] Aplicação "Sistema de Gestão de Mercado" criada
- [ ] Query de teste retornou 10 produtos
- [ ] Você consegue ver as tabelas em SQL Workshop

---

## 🔧 Troubleshooting

### Problema: "Workspace não existe"
**Causa:** Você não criou o workspace corretamente.
**Solução:** Volte ao Passo 5 e repita o processo de criação.

### Problema: "User não tem permissão"
**Causa:** Usuário não tem grants (permissões).
**Solução:** Execute em SQL Developer:
```sql
GRANT CREATE SESSION TO APEX_DEVELOPER;
GRANT CREATE TABLE TO APEX_DEVELOPER;
```

### Problema: "Tabelas não aparecem"
**Causa:** Script SQL não foi executado corretamente.
**Solução:** 
1. Verifique se viu mensagem de sucesso
2. Execute em SQL:
```sql
SELECT * FROM CATEGORIAS;
```
3. Se der erro, execute o script novamente

### Problema: "Erro no script SQL"
**Solução:**
1. Copie a mensagem de erro
2. Revise a linha mencionada no script
3. Verifique se não há caracteres especiais corrompidos
4. Tente executar apenas uma tabela por vez

### Problema: "Banco demora muito para provisionar"
**Solução:** Paciência! Free Tier pode levar até 10 minutos. Recarregue a página a cada 2 minutos.

---

## 📚 Próximos Passos

Agora que seu setup está completo:

1. ✅ **Setup concluído** - Seu banco e APEX estão prontos
2. ⏳ **Próximo:** Desenvolver as páginas APEX
   - Página 1: HOME (Dashboard)
   - Página 10: Produtos
   - Página 20: PDV (Ponto de Venda)
   - Página 30: Vendas
   - Página 40: Estoque

3. ⏳ Você receberá documentação para cada página

---

## 📞 Precisa de Ajuda?

Se tiver problemas:
1. Revise este guia (seção de Troubleshooting)
2. Verifique a senha e credenciais
3. Tente fazer logout e login novamente
4. Limpe o cache do navegador (Ctrl+Shift+Delete)
5. Procure pela documentação oficial:
   - Oracle Cloud: https://cloud.oracle.com/
   - Oracle APEX: https://apex.oracle.com/

---

**Status:** ✅ Pronto para começar!  
**Data:** 13 de Julho de 2026  
**Versão:** 1.0

Parabéns! Você completou o setup do Oracle APEX! 🎉
