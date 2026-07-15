const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
const { db, initDatabase } = require('./database');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

// Middleware
app.use(cors());
app.use(express.json());

// Initialize database
initDatabase();

// ============ AUTENTICAÇÃO ============

app.post('/api/auth/login', (req, res) => {
  const { telefone, nome } = req.body;

  if (!telefone || !nome) {
    return res.status(400).json({ error: 'Telefone e nome são obrigatórios' });
  }

  // Verificar ou criar usuário
  db.get('SELECT * FROM usuarios WHERE telefone = ?', [telefone], (err, user) => {
    if (err) return res.status(500).json({ error: err.message });

    if (!user) {
      // Criar novo usuário
      db.run(
        'INSERT INTO usuarios (telefone, nome) VALUES (?, ?)',
        [telefone, nome],
        function (err) {
          if (err) return res.status(500).json({ error: err.message });

          const token = jwt.sign({ userId: this.lastID, telefone, nome }, JWT_SECRET);
          res.json({ token, userId: this.lastID, nome });
        }
      );
    } else {
      // Usuário existente
      const token = jwt.sign({ userId: user.id, telefone: user.telefone, nome: user.nome }, JWT_SECRET);
      res.json({ token, userId: user.id, nome: user.nome });
    }
  });
});

// Middleware para verificar token
const verifyToken = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Token não fornecido' });

  jwt.verify(token, JWT_SECRET, (err, decoded) => {
    if (err) return res.status(401).json({ error: 'Token inválido' });
    req.userId = decoded.userId;
    req.user = decoded;
    next();
  });
};

// ============ PRODUTOS ============

app.get('/api/produtos', (req, res) => {
  db.all('SELECT * FROM produtos WHERE ativo = 1', (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.get('/api/produtos/:id', (req, res) => {
  db.get('SELECT * FROM produtos WHERE id = ?', [req.params.id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ error: 'Produto não encontrado' });
    res.json(row);
  });
});

app.post('/api/produtos', (req, res) => {
  const { nome, descricao, preco, categoria, imagem } = req.body;

  if (!nome || !preco || !categoria) {
    return res.status(400).json({ error: 'Nome, preço e categoria são obrigatórios' });
  }

  db.run(
    'INSERT INTO produtos (nome, descricao, preco, categoria, imagem) VALUES (?, ?, ?, ?, ?)',
    [nome, descricao, preco, categoria, imagem],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID, nome, preco, categoria });
    }
  );
});

app.put('/api/produtos/:id', (req, res) => {
  const { nome, descricao, preco, categoria, imagem, ativo } = req.body;

  db.run(
    'UPDATE produtos SET nome = ?, descricao = ?, preco = ?, categoria = ?, imagem = ?, ativo = ? WHERE id = ?',
    [nome, descricao, preco, categoria, imagem, ativo, req.params.id],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ updated: this.changes });
    }
  );
});

// ============ PEDIDOS ============

app.post('/api/pedidos', verifyToken, (req, res) => {
  const { itens, tipo_entrega, endereco, bairro, observacoes, tipo_pagamento, valor_total } = req.body;

  if (!itens || itens.length === 0) {
    return res.status(400).json({ error: 'Pedido vazio' });
  }

  db.run(
    'INSERT INTO pedidos (usuario_id, tipo_entrega, endereco, bairro, observacoes, valor_total, tipo_pagamento) VALUES (?, ?, ?, ?, ?, ?, ?)',
    [req.userId, tipo_entrega, endereco, bairro, observacoes, valor_total, tipo_pagamento],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });

      const pedidoId = this.lastID;
      let inserted = 0;

      itens.forEach((item) => {
        db.run(
          'INSERT INTO pedido_itens (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)',
          [pedidoId, item.id, item.quantidade, item.preco],
          (err) => {
            if (err) console.error(err);
            inserted++;
            if (inserted === itens.length) {
              res.json({ pedidoId, status: 'pendente' });
            }
          }
        );
      });
    }
  );
});

app.get('/api/pedidos', verifyToken, (req, res) => {
  db.all(
    `SELECT p.*, u.nome, u.telefone FROM pedidos p
     JOIN usuarios u ON p.usuario_id = u.id
     WHERE p.usuario_id = ?
     ORDER BY p.criado_em DESC`,
    [req.userId],
    (err, rows) => {
      if (err) return res.status(500).json({ error: err.message });
      res.json(rows);
    }
  );
});

app.get('/api/pedidos/:id', verifyToken, (req, res) => {
  db.get(
    'SELECT * FROM pedidos WHERE id = ? AND usuario_id = ?',
    [req.params.id, req.userId],
    (err, pedido) => {
      if (err) return res.status(500).json({ error: err.message });
      if (!pedido) return res.status(404).json({ error: 'Pedido não encontrado' });

      db.all(
        'SELECT pi.*, p.nome FROM pedido_itens pi JOIN produtos p ON pi.produto_id = p.id WHERE pi.pedido_id = ?',
        [req.params.id],
        (err, itens) => {
          if (err) return res.status(500).json({ error: err.message });
          res.json({ ...pedido, itens });
        }
      );
    }
  );
});

app.get('/api/admin/pedidos', (req, res) => {
  db.all(
    `SELECT p.*, u.nome, u.telefone FROM pedidos p
     JOIN usuarios u ON p.usuario_id = u.id
     ORDER BY p.criado_em DESC`,
    (err, rows) => {
      if (err) return res.status(500).json({ error: err.message });
      res.json(rows);
    }
  );
});

app.put('/api/admin/pedidos/:id', (req, res) => {
  const { status } = req.body;

  db.run(
    'UPDATE pedidos SET status = ? WHERE id = ?',
    [status, req.params.id],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ updated: this.changes });
    }
  );
});

// ============ SERVIDOR ============

app.listen(PORT, () => {
  console.log(`🚀 Servidor rodando em http://localhost:${PORT}`);
});

module.exports = app;
