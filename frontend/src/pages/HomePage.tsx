import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { Shield, Users, FileText, AlertTriangle, ChevronRight, ExternalLink } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || '/api'

interface Whistleblower {
  id: number
  slug: string
  name: string
  photo_url?: string
  nationality?: string
  main_revelation?: string
  revelation_year?: number
  status: string
  domains: string[]
  summary: string
  is_featured: boolean
}

interface Case {
  id: number
  slug: string
  name: string
  short_name?: string
  domain: string
  revelation_year: number
  summary: string
  revealer_type?: string
  status: string
  is_featured: boolean
}

interface Stats {
  total_whistleblowers: number
  total_cases: number
  whistleblowers_by_status: Record<string, number>
  cases_by_domain: Record<string, number>
}

const statusColors: Record<string, string> = {
  'libre': 'bg-green-100 text-green-800',
  'exilé': 'bg-amber-100 text-amber-800',
  'emprisonné': 'bg-red-100 text-red-800',
  'en procès': 'bg-orange-100 text-orange-800',
  'réhabilité': 'bg-blue-100 text-blue-800',
  'décédé': 'bg-slate-100 text-slate-800',
}

const statusLabels: Record<string, string> = {
  'libre': '✓ Libre',
  'exilé': '🌍 Exilé',
  'emprisonné': '⛓️ Emprisonné',
  'en procès': '⚖️ En procès',
  'réhabilité': '🏆 Réhabilité',
  'décédé': '✝ Décédé',
}

export default function HomePage() {
  const [whistleblowers, setWhistleblowers] = useState<Whistleblower[]>([])
  const [cases, setCases] = useState<Case[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [wbRes, casesRes, statsRes] = await Promise.all([
          fetch(`${API_URL}/whistleblowers?featured_only=true&limit=6`),
          fetch(`${API_URL}/cases?featured_only=true&limit=4`),
          fetch(`${API_URL}/stats`)
        ])
        
        if (wbRes.ok) setWhistleblowers(await wbRes.json())
        if (casesRes.ok) setCases(await casesRes.json())
        if (statsRes.ok) setStats(await statsRes.json())
      } catch (error) {
        console.error('Erreur lors du chargement:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [])

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28">
          <div className="text-center max-w-4xl mx-auto">
            <div className="flex justify-center mb-6">
              <Shield className="h-16 w-16 text-amber-400" />
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
              Héros de la transparence
            </h1>
            <p className="text-xl md:text-2xl text-slate-300 mb-8 leading-relaxed">
              Ils ont sacrifié leur carrière, leur liberté, parfois leur vie pour nous révéler la vérité.
              <br className="hidden md:block" />
              <span className="text-amber-400 font-semibold">Découvrez leurs histoires.</span>
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/lanceurs"
                className="inline-flex items-center justify-center px-8 py-4 bg-amber-500 hover:bg-amber-400 text-slate-900 font-semibold rounded-xl transition shadow-lg hover:shadow-xl"
              >
                <Users className="mr-2 h-5 w-5" />
                Voir les lanceurs d'alerte
              </Link>
              <Link
                to="/affaires"
                className="inline-flex items-center justify-center px-8 py-4 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-xl transition"
              >
                <FileText className="mr-2 h-5 w-5" />
                Explorer les affaires
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Banner */}
      {stats && (
        <section className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
              <div>
                <div className="text-3xl font-bold text-slate-900">{stats.total_whistleblowers}</div>
                <div className="text-sm text-slate-500">Lanceurs d'alerte</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-slate-900">{stats.total_cases}</div>
                <div className="text-sm text-slate-500">Affaires documentées</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-slate-900">
                  {Object.keys(stats.cases_by_domain).length}
                </div>
                <div className="text-sm text-slate-500">Domaines couverts</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-amber-600">
                  {stats.whistleblowers_by_status['exilé'] || 0}
                </div>
                <div className="text-sm text-slate-500">Toujours en exil</div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Featured Whistleblowers */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-10">
            <div>
              <h2 className="text-3xl font-bold text-slate-900">Lanceurs d'alerte</h2>
              <p className="text-slate-600 mt-1">Ceux qui ont osé parler</p>
            </div>
            <Link
              to="/lanceurs"
              className="hidden sm:flex items-center text-amber-600 hover:text-amber-700 font-medium"
            >
              Voir tous
              <ChevronRight className="ml-1 h-5 w-5" />
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-2xl p-6 animate-pulse">
                  <div className="h-16 w-16 bg-slate-200 rounded-full mb-4" />
                  <div className="h-6 bg-slate-200 rounded w-3/4 mb-2" />
                  <div className="h-4 bg-slate-200 rounded w-1/2 mb-4" />
                  <div className="h-20 bg-slate-200 rounded" />
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {whistleblowers.map((wb) => (
                <Link
                  key={wb.id}
                  to={`/lanceur/${wb.slug}`}
                  className="group bg-white rounded-2xl p-6 shadow-sm hover:shadow-lg transition duration-300 border border-slate-100"
                >
                  <div className="flex items-start gap-4 mb-4">
                    <div className="flex-shrink-0">
                      {wb.photo_url ? (
                        <img
                          src={wb.photo_url}
                          alt={wb.name}
                          className="h-16 w-16 rounded-full object-cover"
                        />
                      ) : (
                        <div className="h-16 w-16 rounded-full bg-slate-200 flex items-center justify-center">
                          <Users className="h-8 w-8 text-slate-400" />
                        </div>
                      )}
                    </div>
                    <div className="flex-grow min-w-0">
                      <h3 className="font-bold text-lg text-slate-900 group-hover:text-amber-600 transition truncate">
                        {wb.name}
                      </h3>
                      <p className="text-sm text-slate-500 truncate">
                        {wb.main_revelation || 'Lanceur d\'alerte'}
                      </p>
                      {wb.revelation_year && (
                        <p className="text-xs text-slate-400">{wb.revelation_year}</p>
                      )}
                    </div>
                  </div>
                  
                  <p className="text-slate-600 text-sm line-clamp-3 mb-4">
                    {wb.summary}
                  </p>
                  
                  <div className="flex items-center justify-between">
                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${
                      statusColors[wb.status] || 'bg-slate-100 text-slate-800'
                    }`}>
                      {statusLabels[wb.status] || wb.status}
                    </span>
                    <ChevronRight className="h-5 w-5 text-slate-300 group-hover:text-amber-500 transition" />
                  </div>
                </Link>
              ))}
            </div>
          )}

          <div className="mt-8 text-center sm:hidden">
            <Link
              to="/lanceurs"
              className="inline-flex items-center text-amber-600 hover:text-amber-700 font-medium"
            >
              Voir tous les lanceurs d'alerte
              <ChevronRight className="ml-1 h-5 w-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Cases */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-10">
            <div>
              <h2 className="text-3xl font-bold text-slate-900">Affaires majeures</h2>
              <p className="text-slate-600 mt-1">Les révélations qui ont changé le monde</p>
            </div>
            <Link
              to="/affaires"
              className="hidden sm:flex items-center text-amber-600 hover:text-amber-700 font-medium"
            >
              Voir toutes
              <ChevronRight className="ml-1 h-5 w-5" />
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[1, 2].map((i) => (
                <div key={i} className="bg-slate-50 rounded-2xl p-6 animate-pulse">
                  <div className="h-6 bg-slate-200 rounded w-3/4 mb-4" />
                  <div className="h-24 bg-slate-200 rounded" />
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {cases.map((c) => (
                <Link
                  key={c.id}
                  to={`/affaire/${c.slug}`}
                  className="group bg-slate-50 hover:bg-slate-100 rounded-2xl p-6 transition duration-300 border border-slate-200"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <span className="inline-block px-2.5 py-1 bg-slate-200 text-slate-700 text-xs font-medium rounded-full mb-2">
                        {c.domain}
                      </span>
                      <h3 className="font-bold text-xl text-slate-900 group-hover:text-amber-600 transition">
                        {c.name}
                      </h3>
                    </div>
                    <span className="text-2xl font-bold text-slate-300">{c.revelation_year}</span>
                  </div>
                  
                  <p className="text-slate-600 text-sm line-clamp-3 mb-4">
                    {c.summary}
                  </p>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-500">
                      {c.revealer_type && `Révélé par : ${c.revealer_type}`}
                    </span>
                    <span className="flex items-center text-amber-600 font-medium opacity-0 group-hover:opacity-100 transition">
                      En savoir plus
                      <ChevronRight className="ml-1 h-4 w-4" />
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          )}

          <div className="mt-8 text-center sm:hidden">
            <Link
              to="/affaires"
              className="inline-flex items-center text-amber-600 hover:text-amber-700 font-medium"
            >
              Voir toutes les affaires
              <ChevronRight className="ml-1 h-5 w-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Why Section */}
      <section className="py-16 bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h2 className="text-3xl font-bold mb-4">Pourquoi ce projet ?</h2>
            <p className="text-slate-300 text-lg">
              Les lanceurs d'alerte sont souvent oubliés après les gros titres.
              Nous documentons leurs histoires pour que leur sacrifice ne soit jamais vain.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 mb-4">
                <AlertTriangle className="h-6 w-6" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Mémoire</h3>
              <p className="text-slate-400 text-sm">
                Préserver la mémoire de ceux qui ont risqué tout pour la vérité
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 mb-4">
                <FileText className="h-6 w-6" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Éducation</h3>
              <p className="text-slate-400 text-sm">
                Comprendre les enjeux des affaires révélées et leur impact
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 mb-4">
                <Shield className="h-6 w-6" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Protection</h3>
              <p className="text-slate-400 text-sm">
                Sensibiliser à l'importance de protéger les lanceurs d'alerte
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 bg-amber-50 border-t border-amber-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-slate-600 mb-4">
            <strong>Sentinelles</strong> est un projet de{' '}
            <a
              href="https://declic.cloud"
              target="_blank"
              rel="noopener noreferrer"
              className="text-amber-600 hover:text-amber-700 font-medium inline-flex items-center"
            >
              Declic.cloud
              <ExternalLink className="ml-1 h-4 w-4" />
            </a>
          </p>
          <p className="text-sm text-slate-500">
            Plateforme citoyenne pour une démocratie plus transparente
          </p>
        </div>
      </section>
    </div>
  )
}
