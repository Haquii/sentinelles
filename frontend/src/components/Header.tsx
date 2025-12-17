import { Link, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { Menu, X, Shield, Search } from 'lucide-react'

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const location = useLocation()
  
  const isActive = (path: string) => location.pathname === path || location.pathname.startsWith(path + '/')

  const navItems = [
    { path: '/lanceurs', label: 'Lanceurs d\'alerte' },
    { path: '/affaires', label: 'Affaires' },
    { path: '/a-propos', label: 'À propos' },
  ]

  return (
    <header className="bg-slate-900 text-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2 hover:opacity-90 transition">
            <Shield className="h-8 w-8 text-amber-400" />
            <div>
              <span className="text-xl font-bold">Sentinelles</span>
              <span className="hidden sm:inline text-xs text-slate-400 ml-2">par Declic.cloud</span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  isActive(item.path)
                    ? 'bg-slate-700 text-white'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                {item.label}
              </Link>
            ))}
            <Link
              to="/recherche"
              className="ml-2 p-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition"
              title="Rechercher"
            >
              <Search className="h-5 w-5" />
            </Link>
          </nav>

          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-slate-800 transition"
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {isMenuOpen && (
          <nav className="md:hidden pb-4 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsMenuOpen(false)}
                className={`block px-4 py-2 rounded-lg text-sm font-medium transition ${
                  isActive(item.path)
                    ? 'bg-slate-700 text-white'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                {item.label}
              </Link>
            ))}
            <Link
              to="/recherche"
              onClick={() => setIsMenuOpen(false)}
              className="flex items-center space-x-2 px-4 py-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition"
            >
              <Search className="h-5 w-5" />
              <span>Rechercher</span>
            </Link>
          </nav>
        )}
      </div>
    </header>
  )
}
