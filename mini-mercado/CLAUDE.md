# 🛒 Mini Mercado no Claude Code

## 🚀 Teste Rápido (1 minuto)

### No Claude Code Web:

1. Abra o repositório `coiluisf/claude`
2. Navegue para `mini-mercado/`
3. Siga os passos abaixo

### Terminal 1 - Backend:
```bash
cd mini-mercado/backend
npm install
npm run seed
npm run dev
```

Backend rodará em **http://localhost:3001**

### Terminal 2 - Frontend:
```bash
cd mini-mercado/frontend
npm install
npm run dev
```

Frontend rodará em **http://localhost:5173**

---

## 🎯 Arquitetura

```
mini-mercado/
├── backend/
│   ├── src/
│   │   ├── server.js       → APIs REST (3001)
│   │   ├── database.js     → SQLite config
│   │   └── seed.js         → Dados de teste
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── App.jsx         → App principal
│   │   ├── pages/          → 5 páginas React
│   │   └── index.css       → Estilos globais
│   └── package.json
├── GUIDE.md                → Guia rápido
└── TESTES.md               → 10 cenários de teste
```

---

## 🔌 APIs Principais

### Autenticação
- `POST /api/auth/login` - Login com telefone + nome

### Produtos
- `GET /api/produtos` - Listar todos
- `GET /api/produtos/:id` - Detalhes
- `POST /api/produtos` - Criar (admin)

### Pedidos
- `POST /api/pedidos` - Criar pedido
- `GET /api/pedidos` - Histórico do cliente
- `GET /api/admin/pedidos` - Todos os pedidos (admin)
- `PUT /api/admin/pedidos/:id` - Atualizar status

---

## 📱 Funcionalidades

✅ **Cliente**
- Login simples (telefone + nome)
- Catálogo com 5 categorias
- Carrinho editável
- Retirada/Entrega
- Histórico de pedidos

✅ **Admin**
- Cadastro de produtos
- Acompanhamento de pedidos
- Notificação de novos pedidos
- Atualização de status em tempo real

---

## 🧪 Testar Agora

### Teste 1: Como Cliente
1. Login: Nome = "João", Telefone = "11999999999"
2. Adicione 3 produtos ao carrinho
3. Faça um pedido (retirada ou entrega)
4. Veja em "Meus Pedidos"

### Teste 2: Como Admin
1. Clique em "Admin"
2. Veja o pedido criado
3. Clique "Confirmar"
4. Mude status para "Pronto"

### Teste 3: Adicionar Produto
1. Na aba "Produtos"
2. Nome: "Pastel Gourmet"
3. Preço: "8.50"
4. Categoria: "Pastéis"
5. Clique "Adicionar"
6. Produto aparece no catálogo

---

## ⚡ Performance

- Frontend: **Vite** (dev server rápido)
- Backend: **Express** (APIs leves)
- Database: **SQLite** (sem setup externo)
- Total de produtos: **21 de exemplo**

---

## 🛠️ Customizações Comuns

### Mudar porta do backend
Edite `backend/.env`:
```
PORT=3001  → Mude para 3002, 3003, etc
```

### Mudar taxa de entrega
Edite `frontend/src/pages/Carrinho.jsx`:
```jsx
const TAXA_ENTREGA = 5.0  // Mude o valor
```

### Mudar nome da loja
Edite `frontend/src/App.jsx`:
```jsx
<h1 className="logo">🛒 Seu Nome Aqui</h1>
```

### Adicionar bairros
Edite `frontend/src/pages/Carrinho.jsx`:
```jsx
const BAIRRO = "Centro"  // Ou implementar dropdown
```

---

## 🐛 Troubleshooting

| Erro | Solução |
|------|---------|
| `Port 3001 in use` | Mude PORT em `.env` ou mate processo: `lsof -i :3001` |
| `npm ERR!` | Delete `node_modules` e `npm install` novamente |
| `Produtos não carregam` | Rode `npm run seed` no backend |
| `CORS error` | Backend não está rodando em 3001 |
| `Database locked` | Feche outras instâncias do backend |

---

## 📊 Dados de Teste

Produtos carregados automaticamente:
- 4 Pastéis
- 5 Salgados
- 4 Bebidas
- 5 Doces
- 3 Congelados

**Total: 21 produtos prontos para testar**

---

## 🚀 Próximos Passos

- [ ] Testar fluxo completo de compra
- [ ] Validar responsividade (mobile)
- [ ] Testar painel admin
- [ ] Adicionar novos produtos via admin
- [ ] Customizar cores/nome da loja
- [ ] Integrar pagamento real (Pix/Stripe)

---

## 📞 Stack Completo

| Componente | Tecnologia |
|-----------|-----------|
| Frontend | React 18 + Vite + CSS3 |
| Backend | Node.js + Express 5 |
| Database | SQLite 3 |
| Auth | JWT |
| Real-time (prep) | Socket.io |

---

**Pronto para testar? Comece pelos 3 comandos acima! 🚀**
