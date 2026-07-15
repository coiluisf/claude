import { useState, useEffect } from 'react'
import './Pedidos.css'

export default function Pedidos({ user }) {
  const [pedidos, setPedidos] = useState([])
  const [loading, setLoading] = useState(true)
  const [pedidoSelecionado, setPedidoSelecionado] = useState(null)

  useEffect(() => {
    buscarPedidos()
  }, [])

  const buscarPedidos = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:3001/api/pedidos', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      const data = await response.json()
      setPedidos(data)
    } catch (err) {
      console.error('Erro ao buscar pedidos:', err)
    } finally {
      setLoading(false)
    }
  }

  const buscarDetalhes = async (pedidoId) => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`http://localhost:3001/api/pedidos/${pedidoId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      const data = await response.json()
      setPedidoSelecionado(data)
    } catch (err) {
      console.error('Erro ao buscar detalhes:', err)
    }
  }

  const getStatusBadge = (status) => {
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

  if (loading) return <div className="loading">Carregando pedidos...</div>

  return (
    <div className="pedidos">
      <h1>📋 Meus Pedidos</h1>

      {pedidos.length === 0 ? (
        <div className="vazio">
          <p>Você ainda não realizou nenhum pedido</p>
        </div>
      ) : (
        <div className="pedidos-lista">
          {pedidos.map(pedido => (
            <div key={pedido.id} className="pedido-card">
              <div className="pedido-header">
                <div className="pedido-id">
                  <h3>Pedido #{pedido.id}</h3>
                  <span className="data">{formatarData(pedido.criado_em)}</span>
                </div>
                <div className="pedido-status">
                  <span
                    className="status-badge"
                    style={{ backgroundColor: getStatusBadge(pedido.status) }}
                  >
                    {pedido.status.charAt(0).toUpperCase() + pedido.status.slice(1)}
                  </span>
                </div>
              </div>

              <div className="pedido-info">
                <p>
                  <strong>Tipo:</strong>{' '}
                  {pedido.tipo_entrega === 'retirada' ? '🏪 Retirada em Loja' : '🚚 Tele-entrega'}
                </p>
                {pedido.tipo_entrega === 'entrega' && (
                  <p>
                    <strong>Endereço:</strong> {pedido.endereco}
                  </p>
                )}
                <p>
                  <strong>Pagamento:</strong> {pedido.tipo_pagamento}
                </p>
              </div>

              <div className="pedido-footer">
                <span className="total">R$ {pedido.valor_total.toFixed(2)}</span>
                <button
                  className="detalhes-btn"
                  onClick={() => buscarDetalhes(pedido.id)}
                >
                  Ver Detalhes
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {pedidoSelecionado && (
        <div className="modal-overlay" onClick={() => setPedidoSelecionado(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Pedido #{pedidoSelecionado.id}</h2>
              <button className="fechar-btn" onClick={() => setPedidoSelecionado(null)}>✕</button>
            </div>

            <div className="modal-content">
              <div className="secao-modal">
                <h3>Informações do Pedido</h3>
                <p><strong>Status:</strong> {pedidoSelecionado.status}</p>
                <p><strong>Data:</strong> {formatarData(pedidoSelecionado.criado_em)}</p>
                <p>
                  <strong>Tipo:</strong>{' '}
                  {pedidoSelecionado.tipo_entrega === 'retirada' ? 'Retirada em Loja' : 'Tele-entrega'}
                </p>
                {pedidoSelecionado.tipo_entrega === 'entrega' && (
                  <p><strong>Endereço:</strong> {pedidoSelecionado.endereco}</p>
                )}
                {pedidoSelecionado.observacoes && (
                  <p><strong>Observações:</strong> {pedidoSelecionado.observacoes}</p>
                )}
              </div>

              <div className="secao-modal">
                <h3>Itens do Pedido</h3>
                <div className="itens-tabela">
                  <div className="tabela-header">
                    <span>Produto</span>
                    <span>Quantidade</span>
                    <span>Preço</span>
                    <span>Total</span>
                  </div>
                  {pedidoSelecionado.itens && pedidoSelecionado.itens.map(item => (
                    <div key={item.id} className="tabela-row">
                      <span>{item.nome}</span>
                      <span>{item.quantidade}</span>
                      <span>R$ {item.preco_unitario.toFixed(2)}</span>
                      <span>R$ {(item.preco_unitario * item.quantidade).toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="secao-modal">
                <div className="resumo-pedido">
                  <div className="resumo-linha">
                    <span>Total:</span>
                    <strong>R$ {pedidoSelecionado.valor_total.toFixed(2)}</strong>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
