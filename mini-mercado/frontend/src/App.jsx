import { useState, useEffect } from 'react'
import './App.css'
import Login from './pages/Login'
import Catalogo from './pages/Catalogo'
import Carrinho from './pages/Carrinho'
import Pedidos from './pages/Pedidos'
import AdminPainel from './pages/AdminPainel'

function App() {
  const [user, setUser] = useState(null)
  const [currentPage, setCurrentPage] = useState('catalogo')
  const [isAdmin, setIsAdmin] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    if (token && userData) {
      setUser(JSON.parse(userData))
    }
  }, [])

  const handleLogin = (userData, token) => {
    setUser(userData)
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(userData))
    setCurrentPage('catalogo')
  }

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsAdmin(false)
    setCurrentPage('catalogo')
  }

  if (!user) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <div className="app">
      <header className="navbar">
        <div className="navbar-container">
          <h1 className="logo">🛒 Mini Mercado</h1>
          <nav className="nav-menu">
            <button
              className={`nav-btn ${currentPage === 'catalogo' ? 'active' : ''}`}
              onClick={() => setCurrentPage('catalogo')}
            >
              Catálogo
            </button>
            <button
              className={`nav-btn ${currentPage === 'carrinho' ? 'active' : ''}`}
              onClick={() => setCurrentPage('carrinho')}
            >
              Carrinho
            </button>
            <button
              className={`nav-btn ${currentPage === 'pedidos' ? 'active' : ''}`}
              onClick={() => setCurrentPage('pedidos')}
            >
              Meus Pedidos
            </button>
            <button
              className={`nav-btn ${isAdmin ? 'active' : ''}`}
              onClick={() => {
                setIsAdmin(!isAdmin)
                if (!isAdmin) setCurrentPage('admin')
              }}
            >
              Admin
            </button>
            <div className="user-info">
              <span>{user.nome}</span>
              <button onClick={handleLogout} className="logout-btn">
                Sair
              </button>
            </div>
          </nav>
        </div>
      </header>

      <main className="main-content">
        {isAdmin ? (
          <AdminPainel />
        ) : (
          <>
            {currentPage === 'catalogo' && <Catalogo />}
            {currentPage === 'carrinho' && <Carrinho user={user} onCheckout={() => setCurrentPage('pedidos')} />}
            {currentPage === 'pedidos' && <Pedidos user={user} />}
          </>
        )}
      </main>
    </div>
  )
}

export default App
