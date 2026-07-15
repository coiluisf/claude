const { db, initDatabase, DB_PATH } = require('./database');
const fs = require('fs');

const produtos = [
  // Pastéis
  { nome: 'Pastel de Carne', descricao: 'Pastel crocante com carne moída temperada', preco: 5.50, categoria: 'Pastéis' },
  { nome: 'Pastel de Queijo', descricao: 'Pastel recheado com queijo derretido', preco: 5.50, categoria: 'Pastéis' },
  { nome: 'Pastel de Palmito', descricao: 'Pastel com palmito e cream cheese', preco: 6.00, categoria: 'Pastéis' },
  { nome: 'Pastel de Frango', descricao: 'Pastel com frango desfiado e tempero especial', preco: 6.00, categoria: 'Pastéis' },

  // Salgados
  { nome: 'Coxinha', descricao: 'Coxinha de frango crocante', preco: 4.50, categoria: 'Salgados' },
  { nome: 'Risólis de Carne', descricao: 'Risólis tradicional de carne moída', preco: 5.00, categoria: 'Salgados' },
  { nome: 'Acarajé', descricao: 'Acarajé feito na hora', preco: 7.00, categoria: 'Salgados' },
  { nome: 'Empada', descricao: 'Empada com caldo de frango', preco: 4.00, categoria: 'Salgados' },
  { nome: 'Bolinha de Queijo', descricao: 'Bolinha de queijo crocante', preco: 3.50, categoria: 'Salgados' },

  // Bebidas
  { nome: 'Refrigerante 2L', descricao: 'Refrigerante gelado 2 litros', preco: 8.00, categoria: 'Bebidas' },
  { nome: 'Suco Natural 500ml', descricao: 'Suco natural de laranja ou morango', preco: 5.00, categoria: 'Bebidas' },
  { nome: 'Água 500ml', descricao: 'Água mineral 500ml', preco: 2.00, categoria: 'Bebidas' },
  { nome: 'Cerveja Artesanal 350ml', descricao: 'Cerveja artesanal selecionada', preco: 12.00, categoria: 'Bebidas' },

  // Doces
  { nome: 'Brigadeiro', descricao: 'Brigadeiro tradicional em potinho', preco: 3.00, categoria: 'Doces' },
  { nome: 'Beijinho', descricao: 'Beijinho de coco crocante', preco: 2.50, categoria: 'Doces' },
  { nome: 'Pudim de Leite Condensado', descricao: 'Pudim caseiro com calda', preco: 8.00, categoria: 'Doces' },
  { nome: 'Bolo de Chocolate', descricao: 'Fatia de bolo de chocolate molhadinho', preco: 6.00, categoria: 'Doces' },
  { nome: 'Torta de Sorvete', descricao: 'Torta gelada de sorvete e chocolate', preco: 10.00, categoria: 'Doces' },

  // Congelados
  { nome: 'Pastel Congelado (5 pç)', descricao: '5 pastéis para levar para casa', preco: 20.00, categoria: 'Congelados' },
  { nome: 'Coxinha Congelada (10 pç)', descricao: '10 coxinhas prontas para fritar', preco: 25.00, categoria: 'Congelados' },
  { nome: 'Pizza Congelada', descricao: 'Pizza inteira congelada', preco: 22.00, categoria: 'Congelados' },
];

const seedDatabase = () => {
  initDatabase();

  db.serialize(() => {
    // Limpar produtos existentes
    db.run('DELETE FROM produtos', (err) => {
      if (err) console.error('Erro ao limpar produtos:', err);
    });

    // Inserir novos produtos
    const stmt = db.prepare('INSERT INTO produtos (nome, descricao, preco, categoria) VALUES (?, ?, ?, ?)');

    produtos.forEach(produto => {
      stmt.run([produto.nome, produto.descricao, produto.preco, produto.categoria], (err) => {
        if (err) console.error('Erro ao inserir produto:', err);
      });
    });

    stmt.finalize();

    db.all('SELECT COUNT(*) as total FROM produtos', (err, rows) => {
      if (err) console.error('Erro:', err);
      else console.log(`✅ ${rows[0].total} produtos inseridos com sucesso!`);
    });
  });
};

// Executar seed
seedDatabase();
