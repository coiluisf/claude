const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = path.join(__dirname, '../data/mercado.db');

const db = new sqlite3.Database(DB_PATH, (err) => {
  if (err) console.error('Database connection error:', err);
  else console.log('Connected to SQLite database');
});

const initDatabase = () => {
  db.serialize(() => {
    // Tabela de produtos
    db.run(`
      CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL,
        categoria TEXT NOT NULL,
        imagem TEXT,
        ativo INTEGER DEFAULT 1,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
        atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Tabela de usuários
    db.run(`
      CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telefone TEXT UNIQUE NOT NULL,
        nome TEXT NOT NULL,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Tabela de pedidos
    db.run(`
      CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        tipo_entrega TEXT NOT NULL,
        endereco TEXT,
        bairro TEXT,
        observacoes TEXT,
        valor_total REAL NOT NULL,
        tipo_pagamento TEXT NOT NULL,
        status TEXT DEFAULT 'pendente',
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
      )
    `);

    // Tabela de itens do pedido
    db.run(`
      CREATE TABLE IF NOT EXISTS pedido_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        FOREIGN KEY(pedido_id) REFERENCES pedidos(id),
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
      )
    `);
  });
};

module.exports = { db, initDatabase, DB_PATH };
