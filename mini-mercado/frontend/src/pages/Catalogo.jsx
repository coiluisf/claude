import { useState, useEffect } from 'react'
import './Catalogo.css'

export default function Catalogo() {
  const [produtos, setProdutos] = useState([])
  const [filtro, setFiltro] = useState('todos')
  const [loading, setLoading] = useState(true)

  const categorias = ['Pastéis', 'Salgados', 'Bebidas', 'Doces', 'Congelados']

  useEffect(() => {
    buscarProdutos()
  }, [])

  const buscarProdutos = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/produtos')
      const data = await response.json()
      setProdutos(data)
    } catch (err) {
      console.error('Erro ao buscar produtos:', err)
    } finally {
      setLoading(false)
    }
  }

  const adicionarAoCarrinho = (produto) => {
    const carrinho = JSON.parse(localStorage.getItem('carrinho') || '[]')
    const item = carrinho.find(p => p.id === produto.id)

    if (item) {
      item.quantidade += 1
    } else {
      carrinho.push({ ...produto, quantidade: 1 })
    }

    localStorage.setItem('carrinho', JSON.stringify(carrinho))
    alert(`${produto.nome} adicionado ao carrinho!`)
  }

  const produtosFiltrados = filtro === 'todos'
    ? produtos
    : produtos.filter(p => p.categoria === filtro)

  if (loading) return <div className="loading">Carregando produtos...</div>

  return (
    <div className="catalogo">
      <h1>📦 Nossos Produtos</h1>

      <div className="filtros">
        <button
          className={`filtro-btn ${filtro === 'todos' ? 'active' : ''}`}
          onClick={() => setFiltro('todos')}
        >
          Todos
        </button>
        {categorias.map(cat => (
          <button
            key={cat}
            className={`filtro-btn ${filtro === cat ? 'active' : ''}`}
            onClick={() => setFiltro(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="produtos-grid">
        {produtosFiltrados.length === 0 ? (
          <p className="vazio">Nenhum produto encontrado</p>
        ) : (
          produtosFiltrados.map(produto => (
            <div key={produto.id} className="produto-card">
              <div className="produto-imagem">
                {produto.imagem ? (
                  <img src={produto.imagem} alt={produto.nome} />
                ) : (
                  <div className="imagem-placeholder">📸</div>
                )}
                <span className="categoria-badge">{produto.categoria}</span>
              </div>
              <div className="produto-info">
                <h3>{produto.nome}</h3>
                <p className="descricao">{produto.descricao}</p>
                <div className="produto-footer">
                  <span className="preco">R$ {produto.preco.toFixed(2)}</span>
                  <button
                    className="adicionar-btn"
                    onClick={() => adicionarAoCarrinho(produto)}
                  >
                    Adicionar
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
