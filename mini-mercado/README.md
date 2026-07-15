# 🛒 Mini Mercado - Sistema de Pedidos

Um protótipo full-stack de um mini mercado com sistema de pedidos, catálogo de produtos e painel administrativo.

## 📋 Funcionalidades

### Cliente
- ✅ Login simples com telefone e nome
- ✅ Catálogo de produtos com filtro por categoria
- ✅ Carrinho de compras
- ✅ Opção de retirada em loja ou tele-entrega
- ✅ Histórico de pedidos
- ✅ Visualização detalhada de pedidos

### Admin
- ✅ Cadastro de produtos
- ✅ Visualização em tempo real dos pedidos
- ✅ Notificação de novos pedidos
- ✅ Atualização de status de pedidos
- ✅ Listagem de produtos cadastrados

## 🛠️ Stack Tecnológico

- **Frontend**: React + Vite + CSS
- **Backend**: Node.js + Express
- **Database**: SQLite
- **Real-time**: Socket.io (preparado para integração)

## 🚀 Como Executar

### Pré-requisitos
- Node.js 16+
- npm ou yarn

### Backend

```bash
cd backend

# Instalar dependências
npm install

# Executar servidor
npm run dev
```

Servidor rodará em `http://localhost:3001`

### Frontend

```bash
cd frontend

# Instalar dependências (se necessário)
npm install

# Executar servidor de desenvolvimento
npm run dev
```

Frontend rodará em `http://localhost:5173`

## 📱 Como Usar

### Cliente

1. **Login**: Insira seu nome e telefone (qualquer número)
2. **Navegar**: Explore o catálogo de produtos
3. **Carrinho**: Adicione produtos ao carrinho
4. **Checkout**: 
   - Escolha retirada em loja ou tele-entrega no Centro
   - Selecione forma de pagamento
   - Confirme o pedido

### Admin

1. **Acessar**: Clique no botão "Admin" na navbar
2. **Gerenciar Pedidos**: 
   - Veja pedidos em tempo real
   - Altere status dos pedidos
   - Receba notificações de novos pedidos
3. **Gerenciar Produtos**:
   - Adicione novos produtos
   - Defina categoria e preço
   - Veja lista de produtos

## 📦 Categorias de Produtos

- Pastéis
- Salgados
- Bebidas
- Doces
- Congelados

## 💰 Preços

- **Taxa de Entrega**: R$ 5,00 (apenas tele-entrega)
- **Retirada em Loja**: Sem taxa adicional

## 🕒 Horários

- **Segunda a Sábado**: 06:30 - 21:00
- (Ainda a implementar validação de horário)

## 📊 Estrutura do Banco de Dados

### Tabelas

- `usuarios` - Dados de clientes
- `produtos` - Catálogo de produtos
- `pedidos` - Pedidos realizados
- `pedido_itens` - Itens de cada pedido

## 🔄 Fluxo de Pedido

1. Cliente faz login
2. Cliente adiciona produtos ao carrinho
3. Cliente escolhe tipo de entrega e pagamento
4. Pedido é criado com status "pendente"
5. Admin vê notificação de novo pedido
6. Admin confirma/prepara/entrega o pedido
7. Cliente visualiza status atualizado

## 🎯 Próximas Melhorias

- [ ] Integração com Pix/Cartão
- [ ] Notificação por SMS/Email
- [ ] Autenticação melhorada
- [ ] Dashboard com gráficos
- [ ] Sistema de avaliação
- [ ] Validação de horário de funcionamento
- [ ] Geolocalização para entrega
- [ ] Persistência de histórico detalhado

## 📝 Notas

- O banco de dados SQLite é criado automaticamente
- Todos os dados são locais (sem backup)
- CORS está habilitado para desenvolvimento local

## 🔐 Segurança

⚠️ Este é um protótipo. Para produção:
- Alterar JWT_SECRET
- Validar inputs com mais rigidez
- Implementar rate limiting
- Usar HTTPS
- Criptografar senhas

---

**Desenvolvido com ❤️ para mercados pequenos**
