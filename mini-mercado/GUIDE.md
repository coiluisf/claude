# 📚 Guia Rápido - Mini Mercado

## 🚀 Começando em 3 passos

### 1️⃣ Instalar Backend

```bash
cd backend
npm install
npm run seed    # Popular com produtos de exemplo
npm run dev     # Iniciar servidor
```

### 2️⃣ Instalar Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

### 3️⃣ Acessar

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:3001

## 💡 Primeiros Passos

### Testar como Cliente

1. Abra http://localhost:5173
2. Digite seu **nome** e **telefone** (qualquer número)
3. Clique em "Entrar"
4. Explore o catálogo de produtos
5. Adicione produtos ao carrinho
6. Vá para checkout:
   - Escolha **Retirada em Loja** ou **Tele-entrega**
   - Se escolher entrega, preencha um endereço
   - Escolha forma de pagamento
   - Clique em "Fazer Pedido"
7. Vá para **Meus Pedidos** para ver o histórico

### Testar como Admin

1. Na mesma página (já logado como cliente)
2. Clique no botão **Admin** na navbar
3. Você verá:
   - **Aba Pedidos**: Todos os pedidos com status em tempo real
     - Pedidos pendentes destacados em amarelo
     - Botão para confirmar/alterar status
   - **Aba Produtos**: Adicione novos produtos
     - Nome, descrição, categoria, preço
     - Veja lista de produtos cadastrados

## 📦 Produtos de Exemplo

O script `npm run seed` adiciona automaticamente:

- **Pastéis** (4 tipos)
- **Salgados** (5 tipos)
- **Bebidas** (4 tipos)
- **Doces** (5 tipos)
- **Congelados** (3 tipos)

## 🔄 Fluxo Completo

1. **Cliente** cria conta com nome + telefone
2. **Cliente** navega catálogo e adiciona ao carrinho
3. **Cliente** faz pedido (retirada ou entrega)
4. **Admin** recebe notificação de novo pedido
5. **Admin** confirma e muda status para "pronto"
6. **Cliente** vê status atualizado em "Meus Pedidos"

## 🎯 Funcionalidades Principais

✅ Login sem senha (só nome + telefone)  
✅ Catálogo com 21 produtos de exemplo  
✅ Filtro por categoria  
✅ Carrinho com edição de quantidades  
✅ Retirada em loja ou tele-entrega  
✅ Histórico de pedidos do cliente  
✅ Painel admin com notificações  
✅ Alteração de status em tempo real  

## 📝 Customizações Comuns

### Mudar nome da loja

Edite `frontend/src/App.jsx`:
```jsx
<h1 className="logo">🛒 Seu Nome Aqui</h1>
```

### Mudar horário de funcionamento

Edite `backend/src/server.js` (ainda não validando):
```js
// Seg à Sáb das 06:30 às 21h
```

### Mudar taxa de entrega

Edite `frontend/src/pages/Carrinho.jsx`:
```jsx
const TAXA_ENTREGA = 5.0  // Altere para outro valor
```

### Mudar bairro de entrega

Edite `frontend/src/pages/Carrinho.jsx`:
```jsx
const BAIRRO = "Centro"  // Altere para seu bairro
```

### Adicionar mais categorias

1. Edite `frontend/src/pages/Catalogo.jsx`:
```jsx
const categorias = ['Pastéis', 'Salgados', 'Bebidas', 'Doces', 'Congelados', 'Nova Categoria']
```

2. Edite `frontend/src/pages/AdminPainel.jsx` (linha similar)

## 🐛 Troubleshooting

### Erro de conexão ao servidor
- ✅ Certifique-se que o backend está rodando em http://localhost:3001
- ✅ Verifique se a porta 3001 não está em uso: `lsof -i :3001`

### Produtos não aparecem
- ✅ Rode `npm run seed` no diretório backend
- ✅ Abra o navegador (pode estar em cache)

### Erro de banco de dados
- ✅ Delete `backend/data/mercado.db`
- ✅ Reinicie o servidor

### Login não funciona
- ✅ Verifique se o backend está respondendo
- ✅ Teste em http://localhost:3001/api/produtos (deve retornar JSON)

## 📱 Responsividade

O sistema é totalmente responsivo:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🔐 Notas Importante

⚠️ **Este é um protótipo!** Para produção:
- Altere `JWT_SECRET` em `backend/.env`
- Implemente autenticação real
- Use HTTPS
- Validação de inputs rigorosa
- Banco de dados profissional (PostgreSQL)

## 💾 Estrutura de Pastas

```
mini-mercado/
├── backend/
│   ├── src/
│   │   ├── database.js   (SQLite config)
│   │   ├── server.js     (APIs Express)
│   │   └── seed.js       (Produtos exemplo)
│   ├── package.json
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Catalogo.jsx
│   │   │   ├── Carrinho.jsx
│   │   │   ├── Pedidos.jsx
│   │   │   └── AdminPainel.jsx
│   │   └── (CSS files)
│   └── package.json
└── README.md
```

## 📞 Suporte

Qualquer dúvida, abra uma issue ou comece a customizar! 🚀
