import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { LogOut, Menu, MessageSquare, Scale, Users, X, Upload, FileOutput } from 'lucide-react'
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

  const navLinks = [
    { to: '/chat', icon: MessageSquare, label: 'Chat' },
    { to: '/documents', icon: Upload, label: 'My Docs' },
    { to: '/generate', icon: FileOutput, label: 'Generate' },
    { to: '/experts', icon: Users, label: 'Experts' },
  ]

  return (
    <nav className="glass fixed left-0 right-0 top-0 z-50 border-b border-white/10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <div className="flex h-16 items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <Scale className="h-7 w-7 text-gold-500" />
            <span className="font-serif text-xl font-bold gradient-text">LAWAI</span>
          </Link>

          <div className="hidden items-center space-x-1 md:flex">
            {navLinks.map(({ to, icon: Icon, label }) => (
              <Link
                key={to}
                to={to}
                className={`rounded-lg px-4 py-2 text-sm font-medium transition-all ${
                  isActive(to)
                    ? 'bg-gold-500/20 text-gold-400'
                    : 'text-gray-400 hover:bg-dark-700 hover:text-gold-400'
                }`}
              >
                <span className="flex items-center gap-2">
                  <Icon className="h-4 w-4" />
                  {label}
                </span>
              </Link>
            ))}
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
                <Link to="/login" className="btn-outline px-4 py-2 text-sm">Login</Link>
                <Link to="/register" className="btn-gold px-4 py-2 text-sm">Get Started</Link>
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
          <div className="space-y-1 pb-4 md:hidden">
            {navLinks.map(({ to, icon: Icon, label }) => (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive(to) ? 'text-gold-400 bg-gold-500/10' : 'text-gray-300 hover:text-gold-400'
                }`}
                onClick={() => setMenuOpen(false)}
              >
                <Icon className="h-4 w-4" />
                {label}
              </Link>
            ))}
            {user ? (
              <button
                onClick={() => { handleLogout(); setMenuOpen(false) }}
                className="flex items-center gap-2 w-full px-4 py-2.5 text-left text-red-400 text-sm"
              >
                <LogOut className="h-4 w-4" />
                Logout
              </button>
            ) : (
              <div className="flex gap-2 px-4 pt-2">
                <Link to="/login" className="btn-outline px-4 py-2 text-sm flex-1 text-center" onClick={() => setMenuOpen(false)}>Login</Link>
                <Link to="/register" className="btn-gold px-4 py-2 text-sm flex-1 text-center" onClick={() => setMenuOpen(false)}>Sign Up</Link>
              </div>
            )}
          </div>
        )}
      </div>
    </nav>
  )
}
