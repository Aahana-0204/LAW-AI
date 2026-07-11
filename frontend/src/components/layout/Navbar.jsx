import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { LogOut, Menu, MessageSquare, Scale, Users, X } from 'lucide-react'
import { useAuth } from '../../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const isActive = (path) => location.pathname === path

  return (
    <nav className="glass fixed left-0 right-0 top-0 z-50 border-b border-white/10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <div className="flex h-16 items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <Scale className="h-7 w-7 text-gold-500" />
            <span className="font-serif text-xl font-bold gradient-text">LAWAI</span>
          </Link>

          <div className="hidden items-center space-x-1 md:flex">
            <Link
              to="/chat"
              className={`rounded-lg px-4 py-2 text-sm font-medium transition-all ${
                isActive('/chat')
                  ? 'bg-gold-500/20 text-gold-400'
                  : 'text-gray-400 hover:bg-dark-700 hover:text-gold-400'
              }`}
            >
              <span className="flex items-center gap-2">
                <MessageSquare className="h-4 w-4" />
                Chat
              </span>
            </Link>
            <Link
              to="/experts"
              className={`rounded-lg px-4 py-2 text-sm font-medium transition-all ${
                isActive('/experts')
                  ? 'bg-gold-500/20 text-gold-400'
                  : 'text-gray-400 hover:bg-dark-700 hover:text-gold-400'
              }`}
            >
              <span className="flex items-center gap-2">
                <Users className="h-4 w-4" />
                Experts
              </span>
            </Link>
          </div>

          <div className="hidden items-center space-x-3 md:flex">
            {user ? (
              <>
                <span className="text-sm text-gray-400">
                  Hi, <span className="font-medium text-gold-400">{user.name?.split(' ')[0]}</span>
                </span>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-gray-400 transition-colors hover:bg-red-500/10 hover:text-red-400"
                >
                  <LogOut className="h-4 w-4" />
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn-outline px-4 py-2 text-sm">
                  Login
                </Link>
                <Link to="/register" className="btn-gold px-4 py-2 text-sm">
                  Get Started
                </Link>
              </>
            )}
          </div>

          <button
            className="p-2 text-gray-400 hover:text-gold-400 md:hidden"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {menuOpen && (
          <div className="space-y-2 pb-4 md:hidden">
            <Link
              to="/chat"
              className="block px-4 py-2 text-gray-300 hover:text-gold-400"
              onClick={() => setMenuOpen(false)}
            >
              Chat
            </Link>
            <Link
              to="/experts"
              className="block px-4 py-2 text-gray-300 hover:text-gold-400"
              onClick={() => setMenuOpen(false)}
            >
              Experts
            </Link>
            {user ? (
              <button
                onClick={() => {
                  handleLogout()
                  setMenuOpen(false)
                }}
                className="block w-full px-4 py-2 text-left text-red-400"
              >
                Logout
              </button>
            ) : (
              <>
                <Link
                  to="/login"
                  className="block px-4 py-2 text-gray-300"
                  onClick={() => setMenuOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="block px-4 py-2 font-medium text-gold-400"
                  onClick={() => setMenuOpen(false)}
                >
                  Get Started
                </Link>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  )
}
