import { useState, useEffect } from 'react'
import './Carrinho.css'

export default function Carrinho({ user, onCheckout }) {
  const [carrinho, setCarrinho] = useState([])
  const [tipoEntrega, setTipoEntrega] = useState('retirada')
  const [endereco, setEndereco] = useState('')
  const [observacoes, setObservacoes] = useState('')
  const [tipoPagamento, setTipoPagamento] = useState('dinheiro')
  const [loading, setLoading] = useState(false)

  const TAXA_ENTREGA = 5.0
  const BAIRRO = "Centro"

  useEffect(() => {
    const carrinho = JSON.parse(localStorage.getItem('carrinho') || '[]')
    setCarrinho(carrinho)
  }, [])

  const atualizarQuantidade = (id, quantidade) => {
    if (quantidade <= 0) {
      removerItem(id)
      return
    }

    const novoCarrinho = carrinho.map(item =>
      item.id === id ? { ...item, quantidade } : item
    )
    setCarrinho(novoCarrinho)
    localStorage.setItem('carrinho', JSON.stringify(novoCarrinho))
  }

  const removerItem = (id) => {
    const novoCarrinho = carrinho.filter(item => item.id !== id)
    setCarrinho(novoCarrinho)
    localStorage.setItem('carrinho', JSON.stringify(novoCarrinho))
  }

  const calcularTotal = () => {
    const subtotal = carrinho.reduce((sum, item) => sum + (item.preco * item.quantidade), 0)
    const taxa = tipoEntrega === 'entrega' ? TAXA_ENTREGA : 0
    return subtotal + taxa
  }

  const handleCheckout = async () => {
    if (carrinho.length === 0) {
      alert('Carrinho vazio!')
      return
    }

    if (tipoEntrega === 'entrega' && !endereco) {
      alert('Por favor, informe o endereço de entrega')
      return
    }

    setLoading(true)

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:3001/api/pedidos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          itens: carrinho,
          tipo_entrega: tipoEntrega,
          endereco: tipoEntrega === 'entrega' ? endereco : null,
          bairro: tipoEntrega === 'entrega' ? BAIRRO : null,
          observacoes,
          tipo_pagamento: tipoPagamento,
          valor_total: calcularTotal()
        })
      })

      const data = await response.json()

      if (!response.ok) {
        alert(data.error || 'Erro ao processar pedido')
        return
      }

      alert('Pedido criado com sucesso!')
      localStorage.removeItem('carrinho')
      setCarrinho([])
      onCheckout()
    } catch (err) {
      alert('Erro ao processar pedido')
    } finally {
      setLoading(false)
    }
  }

  if (carrinho.length === 0) {
    return (
      <div className="carrinho-vazio">
        <h1>🛒 Seu Carrinho</h1>
        <div className="vazio">
          <p>Carrinho vazio</p>
          <p>Adicione produtos do catálogo para começar!</p>
        </div>
      </div>
    )
  }

  const subtotal = carrinho.reduce((sum, item) => sum + (item.preco * item.quantidade), 0)
  const taxa = tipoEntrega === 'entrega' ? TAXA_ENTREGA : 0
  const total = calcularTotal()

  return (
    <div className="carrinho">
      <h1>🛒 Seu Carrinho</h1>

      <div className="carrinho-container">
        <div className="carrinho-items">
          {carrinho.map(item => (
            <div key={item.id} className="carrinho-item">
              <div className="item-info">
                <h3>{item.nome}</h3>
                <p className="categoria">{item.categoria}</p>
              </div>
              <div className="item-preco">
                <span>R$ {item.preco.toFixed(2)}</span>
              </div>
              <div className="item-quantidade">
                <button onClick={() => atualizarQuantidade(item.id, item.quantidade - 1)}>−</button>
                <input
                  type="number"
                  min="1"
                  value={item.quantidade}
                  onChange={(e) => atualizarQuantidade(item.id, parseInt(e.target.value))}
                />
                <button onClick={() => atualizarQuantidade(item.id, item.quantidade + 1)}>+</button>
              </div>
              <div className="item-total">
                R$ {(item.preco * item.quantidade).toFixed(2)}
              </div>
              <button
                className="remover-btn"
                onClick={() => removerItem(item.id)}
              >
                🗑️
              </button>
            </div>
          ))}
        </div>

        <div className="checkout-panel">
          <h2>Resumo do Pedido</h2>

          <div className="secao">
            <h3>Tipo de Entrega</h3>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  value="retirada"
                  checked={tipoEntrega === 'retirada'}
                  onChange={(e) => setTipoEntrega(e.target.value)}
                />
                Retirada em Loja
              </label>
              <label>
                <input
                  type="radio"
                  value="entrega"
                  checked={tipoEntrega === 'entrega'}
                  onChange={(e) => setTipoEntrega(e.target.value)}
                />
                Tele-entrega no {BAIRRO}
              </label>
            </div>
          </div>

          {tipoEntrega === 'entrega' && (
            <div className="secao">
              <label>Endereço de Entrega</label>
              <input
                type="text"
                value={endereco}
                onChange={(e) => setEndereco(e.target.value)}
                placeholder="Rua, número, complemento"
              />
            </div>
          )}

          <div className="secao">
            <label>Observações (opcional)</label>
            <textarea
              value={observacoes}
              onChange={(e) => setObservacoes(e.target.value)}
              placeholder="Adicione observações sobre o pedido"
              rows="3"
            />
          </div>

          <div className="secao">
            <h3>Forma de Pagamento</h3>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  value="dinheiro"
                  checked={tipoPagamento === 'dinheiro'}
                  onChange={(e) => setTipoPagamento(e.target.value)}
                />
                Dinheiro
              </label>
              <label>
                <input
                  type="radio"
                  value="pix"
                  checked={tipoPagamento === 'pix'}
                  onChange={(e) => setTipoPagamento(e.target.value)}
                />
                Pix
              </label>
              <label>
                <input
                  type="radio"
                  value="cartao"
                  checked={tipoPagamento === 'cartao'}
                  onChange={(e) => setTipoPagamento(e.target.value)}
                />
                Cartão
              </label>
            </div>
          </div>

          <div className="resumo">
            <div className="resumo-linha">
              <span>Subtotal:</span>
              <span>R$ {subtotal.toFixed(2)}</span>
            </div>
            {tipoEntrega === 'entrega' && (
              <div className="resumo-linha">
                <span>Taxa de Entrega:</span>
                <span>R$ {taxa.toFixed(2)}</span>
              </div>
            )}
            <div className="resumo-linha total">
              <span>Total:</span>
              <span>R$ {total.toFixed(2)}</span>
            </div>
          </div>

          <button
            className="checkout-btn"
            onClick={handleCheckout}
            disabled={loading}
          >
            {loading ? 'Processando...' : 'Fazer Pedido'}
          </button>
        </div>
      </div>
    </div>
  )
}
