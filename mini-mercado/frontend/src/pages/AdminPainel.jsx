import { useState, useEffect } from 'react'
import './AdminPainel.css'

export default function AdminPainel() {
  const [abaPrincipal, setAbaPrincipal] = useState('pedidos')
  const [pedidos, setPedidos] = useState([])
  const [produtos, setProdutos] = useState([])
  const [formProduto, setFormProduto] = useState({
    nome: '',
    descricao: '',
    preco: '',
    categoria: 'Pastéis'
  })
  const [loading, setLoading] = useState(false)
  const [notificacao, setNotificacao] = useState(null)
  const [novosPedidosNotificacao, setNovosPedidosNotificacao] = useState([])

  const categorias = ['Pastéis', 'Salgados', 'Bebidas', 'Doces', 'Congelados']

  useEffect(() => {
    buscarDados()
    const intervalo = setInterval(buscarDados, 5000)
    return () => clearInterval(intervalo)
  }, [])

  const buscarDados = async () => {
    try {
      const [pedidosRes, produtosRes] = await Promise.all([
        fetch('http://localhost:3001/api/admin/pedidos'),
        fetch('http://localhost:3001/api/produtos')
      ])

      const pedidosData = await pedidosRes.json()
      const produtosData = await produtosRes.json()

      setPedidos(pedidosData)
      setProdutos(produtosData)

      // Verificar novos pedidos pendentes
      const novosPendentes = pedidosData.filter(p => p.status === 'pendente')
      if (novosPendentes.length > 0) {
        setNovosPedidosNotificacao(novosPendentes)
      }
    } catch (err) {
      console.error('Erro ao buscar dados:', err)
    }
  }

  const handleAddProduto = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch('http://localhost:3001/api/produtos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formProduto,
          preco: parseFloat(formProduto.preco)
        })
      })

      if (!response.ok) throw new Error('Erro ao adicionar produto')

      setFormProduto({ nome: '', descricao: '', preco: '', categoria: 'Pastéis' })
      setNotificacao('Produto adicionado com sucesso!')
      buscarDados()
      setTimeout(() => setNotificacao(null), 3000)
    } catch (err) {
      setNotificacao('Erro ao adicionar produto')
    } finally {
      setLoading(false)
    }
  }

  const atualizarStatusPedido = async (pedidoId, novoStatus) => {
    try {
      await fetch(`http://localhost:3001/api/admin/pedidos/${pedidoId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: novoStatus })
      })

      setNotificacao('Pedido atualizado com sucesso!')
      buscarDados()
      setTimeout(() => setNotificacao(null), 3000)
    } catch (err) {
      setNotificacao('Erro ao atualizar pedido')
    }
  }

  const getStatusColor = (status) => {
    const cores = {
      'pendente': '#FFC107',
      'confirmado': '#2196F3',
      'pronto': '#4CAF50',
      'entregue': '#8BC34A',
      'cancelado': '#F44336'
    }
    return cores[status] || '#999'
  }

  const formatarData = (data) => {
    return new Date(data).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const pedidosPendentes = pedidos.filter(p => p.status === 'pendente')

  return (
    <div className="admin-painel">
      <h1>⚙️ Painel de Administração</h1>

      {novosPedidosNotificacao.length > 0 && (
        <div className="notificacao-nova-pedido">
          <div className="notificacao-conteudo">
            <span>🔔 {novosPedidosNotificacao.length} novo(s) pedido(s) pendente(s)!</span>
            <button onClick={() => setNovosPedidosNotificacao([])}>✕</button>
          </div>
        </div>
      )}

      {notificacao && (
        <div className={`notificacao ${notificacao.includes('Erro') ? 'erro' : 'sucesso'}`}>
          {notificacao}
        </div>
      )}

      <div className="abas">
        <button
          className={`aba-btn ${abaPrincipal === 'pedidos' ? 'active' : ''}`}
          onClick={() => setAbaPrincipal('pedidos')}
        >
          📋 Pedidos {pedidosPendentes.length > 0 && `(${pedidosPendentes.length})`}
        </button>
        <button
          className={`aba-btn ${abaPrincipal === 'produtos' ? 'active' : ''}`}
          onClick={() => setAbaPrincipal('produtos')}
        >
          📦 Produtos
        </button>
      </div>

      <div className="aba-conteudo">
        {abaPrincipal === 'pedidos' && (
          <div className="pedidos-admin">
            <h2>Gerenciar Pedidos</h2>

            {pedidosPendentes.length > 0 && (
              <div className="secao-critica">
                <h3>⚠️ Pedidos Pendentes ({pedidosPendentes.length})</h3>
                <div className="pedidos-grid">
                  {pedidosPendentes.map(pedido => (
                    <div key={pedido.id} className="pedido-admin pendente">
                      <div className="pedido-cabecalho">
                        <span className="pedido-id">Pedido #{pedido.id}</span>
                        <span className="cliente">{pedido.nome}</span>
                      </div>
                      <div className="pedido-detalhes">
                        <p>📞 {pedido.telefone}</p>
                        <p>
                          {pedido.tipo_entrega === 'retirada'
                            ? '🏪 Retirada em Loja'
                            : `🚚 Entrega - ${pedido.endereco}`}
                        </p>
                        <p>💰 R$ {pedido.valor_total.toFixed(2)}</p>
                        <p className="data">{formatarData(pedido.criado_em)}</p>
                      </div>
                      <div className="pedido-acoes">
                        <button
                          className="btn-confirmar"
                          onClick={() => atualizarStatusPedido(pedido.id, 'confirmado')}
                        >
                          Confirmar
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="secao-pedidos">
              <h3>Todos os Pedidos</h3>
              <div className="pedidos-tabela">
                <div className="tabela-header">
                  <span>ID</span>
                  <span>Cliente</span>
                  <span>Tipo</span>
                  <span>Valor</span>
                  <span>Status</span>
                  <span>Ações</span>
                </div>
                {pedidos.map(pedido => (
                  <div key={pedido.id} className="tabela-row">
                    <span>#{pedido.id}</span>
                    <span>{pedido.nome}</span>
                    <span>{pedido.tipo_entrega === 'retirada' ? 'Retirada' : 'Entrega'}</span>
                    <span>R$ {pedido.valor_total.toFixed(2)}</span>
                    <span
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(pedido.status) }}
                    >
                      {pedido.status}
                    </span>
                    <div className="status-select">
                      <select
                        value={pedido.status}
                        onChange={(e) => atualizarStatusPedido(pedido.id, e.target.value)}
                      >
                        <option value="pendente">Pendente</option>
                        <option value="confirmado">Confirmado</option>
                        <option value="pronto">Pronto</option>
                        <option value="entregue">Entregue</option>
                        <option value="cancelado">Cancelado</option>
                      </select>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {abaPrincipal === 'produtos' && (
          <div className="produtos-admin">
            <h2>Gerenciar Produtos</h2>

            <div className="form-container">
              <h3>Adicionar Novo Produto</h3>
              <form onSubmit={handleAddProduto}>
                <div className="form-group">
                  <label>Nome do Produto</label>
                  <input
                    type="text"
                    value={formProduto.nome}
                    onChange={(e) => setFormProduto({ ...formProduto, nome: e.target.value })}
                    placeholder="Ex: Pastel de Carne"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Descrição</label>
                  <input
                    type="text"
                    value={formProduto.descricao}
                    onChange={(e) => setFormProduto({ ...formProduto, descricao: e.target.value })}
                    placeholder="Descrição do produto"
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Categoria</label>
                    <select
                      value={formProduto.categoria}
                      onChange={(e) => setFormProduto({ ...formProduto, categoria: e.target.value })}
                    >
                      {categorias.map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Preço (R$)</label>
                    <input
                      type="number"
                      step="0.01"
                      value={formProduto.preco}
                      onChange={(e) => setFormProduto({ ...formProduto, preco: e.target.value })}
                      placeholder="10.50"
                      required
                    />
                  </div>
                </div>

                <button type="submit" disabled={loading} className="btn-submit">
                  {loading ? 'Adicionando...' : 'Adicionar Produto'}
                </button>
              </form>
            </div>

            <div className="produtos-lista">
              <h3>Produtos Cadastrados ({produtos.length})</h3>
              <div className="produtos-grid-admin">
                {produtos.map(produto => (
                  <div key={produto.id} className="produto-admin-card">
                    <h4>{produto.nome}</h4>
                    <p className="desc">{produto.descricao}</p>
                    <p className="categoria">{produto.categoria}</p>
                    <div className="preco-admin">R$ {produto.preco.toFixed(2)}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
