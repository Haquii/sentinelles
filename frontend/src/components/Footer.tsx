import { Link } from 'react-router-dom'
import { Shield, ExternalLink, Heart } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-slate-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-2">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              <Shield className="h-8 w-8 text-amber-400" />
              <span className="text-xl font-bold">Sentinelles</span>
            </Link>
            <p className="text-slate-400 text-sm max-w-md">
              Une plateforme dédiée à la mémoire des lanceurs d'alerte. 
              Parce que leur courage mérite d'être documenté et honoré.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Explorer</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/lanceurs" className="text-slate-400 hover:text-white transition">
                  Lanceurs d'alerte
                </Link>
              </li>
              <li>
                <Link to="/affaires" className="text-slate-400 hover:text-white transition">
                  Affaires majeures
                </Link>
              </li>
              <li>
                <Link to="/a-propos" className="text-slate-400 hover:text-white transition">
                  À propos
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Declic.cloud</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a
                  href="https://declic.cloud"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-slate-400 hover:text-white transition inline-flex items-center"
                >
                  Site principal
                  <ExternalLink className="ml-1 h-3 w-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://ethiscan.declic.cloud"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-slate-400 hover:text-white transition inline-flex items-center"
                >
                  EthiScan
                  <ExternalLink className="ml-1 h-3 w-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://visupol.declic.cloud"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-slate-400 hover:text-white transition inline-flex items-center"
                >
                  VisuPol
                  <ExternalLink className="ml-1 h-3 w-3" />
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-slate-500">
          <p>
            © {new Date().getFullYear()} Sentinelles — Un projet{' '}
            <a href="https://declic.cloud" className="text-amber-400 hover:text-amber-300">
              Declic.cloud
            </a>
          </p>
          <p className="flex items-center mt-2 md:mt-0">
            Fait avec <Heart className="h-4 w-4 mx-1 text-red-500" /> par des citoyens engagés
          </p>
        </div>
      </div>
    </footer>
  )
}
