# 🧪 Guia de Testes - Mini Mercado

## 🚀 Setup Rápido

### Passo 1: Instalar e Rodar Backend
```bash
cd mini-mercado/backend
npm install
npm run seed    # Popula com 21 produtos
npm run dev     # Porta 3001
```

### Passo 2: Instalar e Rodar Frontend
```bash
cd mini-mercado/frontend
npm install
npm run dev     # Porta 5173
```

### Passo 3: Abrir no Navegador
http://localhost:5173

---

## 👥 Cenários de Teste

### ✅ Teste 1: Login e Navegação

**Passos:**
1. Abra http://localhost:5173
2. Insira:
   - Nome: "João Silva"
   - Telefone: "11999999999"
3. Clique "Entrar"

**Esperado:**
- ✅ Login bem-sucedido
- ✅ Redirecionado para catálogo
- ✅ Nome exibido na navbar
- ✅ Botão "Sair" visível

---

### ✅ Teste 2: Catálogo e Filtros

**Passos:**
1. Na página de catálogo
2. Clique em "Pastéis" (filtro)
3. Verifique se mostra apenas pastéis
4. Clique em "Todos"
5. Verifique se voltou a mostrar todos

**Esperado:**
- ✅ Produtos filtrados corretamente
- ✅ Contador de produtos atualiza
- ✅ Cards com preço, descrição
- ✅ Botão "Adicionar" funciona

---

### ✅ Teste 3: Carrinho - Adicionar Itens

**Passos:**
1. No catálogo, clique "Adicionar" em 3 produtos diferentes
2. Você deve receber alerts
3. Clique na aba "Carrinho"

**Esperado:**
- ✅ Alert confirma adição
- ✅ 3 itens no carrinho
- ✅ Preço unitário mostrado
- ✅ Quantidade editável

---

### ✅ Teste 4: Carrinho - Editar Quantidades

**Passos:**
1. No carrinho, clique no botão "+" para aumentar
2. Clique no botão "−" para diminuir
3. Digite um número direto no input
4. Clique no botão 🗑️ para remover

**Esperado:**
- ✅ Quantidade atualiza
- ✅ Total recalcula automaticamente
- ✅ Item é removido
- ✅ Se quantidade = 0, item remove

---

### ✅ Teste 5: Checkout - Retirada em Loja

**Passos:**
1. No carrinho, selecione "Retirada em Loja"
2. O campo de endereço **desaparece**
3. Taxa de entrega **não aparece**
4. Escolha forma de pagamento (Dinheiro, Pix ou Cartão)
5. Clique "Fazer Pedido"

**Esperado:**
- ✅ Pedido criado com sucesso
- ✅ Alert de confirmação
- ✅ Carrinho é limpo
- ✅ Redireciona para "Meus Pedidos"

---

### ✅ Teste 6: Checkout - Tele-entrega

**Passos:**
1. Adicione produtos ao carrinho
2. Selecione "Tele-entrega no Centro"
3. Campo de endereço aparece
4. Digite um endereço (ex: "Rua A, 123")
5. Taxa de R$ 5,00 aparece no resumo
6. Escolha forma de pagamento
7. Clique "Fazer Pedido"

**Esperado:**
- ✅ Campo de endereço obrigatório
- ✅ Taxa de R$ 5,00 adicionada
- ✅ Total correto (subtotal + taxa)
- ✅ Pedido criado
- ✅ Alerta de sucesso

---

### ✅ Teste 7: Histórico de Pedidos

**Passos:**
1. Clique "Meus Pedidos" na navbar
2. Você deve ver os pedidos criados
3. Clique "Ver Detalhes" em um pedido

**Esperado:**
- ✅ Lista de pedidos carregada
- ✅ Status exibido com cor correta
- ✅ Modal com detalhes abre
- ✅ Mostra itens do pedido
- ✅ Mostra valor total correto

---

### ✅ Teste 8: Admin - Adicionar Produto

**Passos:**
1. Clique botão "Admin" na navbar
2. Você vê painel admin
3. Na aba "Produtos", preencha:
   - Nome: "Pastel de Palmito Premium"
   - Descrição: "Com cream cheese extra"
   - Categoria: "Pastéis"
   - Preço: "7.50"
4. Clique "Adicionar Produto"

**Esperado:**
- ✅ Notificação de sucesso
- ✅ Produto aparece na lista
- ✅ Catálogo atualiza automaticamente
- ✅ Novo produto aparece em "Todos"

---

### ✅ Teste 9: Admin - Acompanhar Pedidos

**Passos:**
1. Na aba "Pedidos", você vê todos os pedidos
2. Pedidos pendentes estão destacados em amarelo
3. Clique "Confirmar" em um pedido pendente
4. Status muda para "confirmado"
5. Use o dropdown para mudar status (Pronto, Entregue, etc)

**Esperado:**
- ✅ Pedidos pendentes destacados
- ✅ Status atualiza em tempo real
- ✅ Notificação de sucesso
- ✅ Dropdown funciona para todos os status

---

### ✅ Teste 10: Responsividade

**Passos:**
1. Abra a página em navegador normal
2. Pressione F12 (DevTools)
3. Clique no ícone de responsividade (📱)
4. Teste em diferentes tamanhos:
   - iPhone 12 (390px)
   - iPad (768px)
   - Desktop (1200px)

**Esperado:**
- ✅ Layout ajusta para mobile
- ✅ Menu reduz/adapta
- ✅ Grid de produtos responsivo
- ✅ Modals funcionam no mobile
- ✅ Sem scroll horizontal

---

## 🐛 Testes de Edge Cases

### ❓ Teste: Carrinho Vazio

**Passos:**
1. Vá para carrinho vazio
2. Clique "Fazer Pedido"

**Esperado:**
- ✅ Alert: "Carrinho vazio!"
- ✅ Pedido não é criado

---

### ❓ Teste: Entrega sem Endereço

**Passos:**
1. Adicione produtos
2. Escolha "Tele-entrega"
3. Deixe endereço vazio
4. Clique "Fazer Pedido"

**Esperado:**
- ✅ Alert: "Por favor, informe o endereço"
- ✅ Pedido não é criado

---

### ❓ Teste: Login com Telefone Duplicado

**Passos:**
1. Primeira vez: Login com "João" e "11999999999"
2. Saia e faça novo login com mesmo telefone, nome diferente "Maria"

**Esperado:**
- ✅ Login aceita (usuário existente reutilizado)
- ✅ Histórico de pedidos do João continua visível se usar mesmo telefone

---

## 📊 Checklist Final

- [ ] Login funciona
- [ ] Catálogo mostra todos os produtos
- [ ] Filtros funcionam
- [ ] Adicionar ao carrinho funciona
- [ ] Editar quantidades funciona
- [ ] Retirada em loja funciona
- [ ] Tele-entrega funciona
- [ ] Taxa de entrega correta
- [ ] Histórico de pedidos funciona
- [ ] Modal de detalhes funciona
- [ ] Admin adiciona produtos
- [ ] Admin vê pedidos
- [ ] Status atualiza em tempo real
- [ ] Notificação de novo pedido aparece
- [ ] Layout responsivo no mobile
- [ ] Cores e UX estão boas

---

## 🎯 Melhorias para Feedback

Após testar, você pode pedir ajustes em:

1. **Design**: Cores, fonts, spacing
2. **Funcionalidades**: Novos campos, validações
3. **Performance**: Otimizações de loading
4. **Integrações**: Pix, Stripe, SMS, Email
5. **Categorias**: Adicionar/remover categorias
6. **Bairros**: Múltiplos bairros de entrega
7. **Horários**: Validar horário de funcionamento

---

## 🚨 Se der Erro

### Backend não conecta
```bash
# Verifique se rodando em 3001
lsof -i :3001

# Reinicie
npm run dev
```

### Produtos não aparecem
```bash
# Rode seed novamente
npm run seed
```

### Banco de dados corrompido
```bash
# Delete e recrie
rm backend/data/mercado.db
npm run dev
npm run seed
```

---

**Bom teste! 🚀**
