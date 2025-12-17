import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Search, Users, FileText, Building2 } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || '/api'

interface SearchResult {
  id: number
  slug: string
  name: string
  type: string
}

interface SearchResults {
  query: string
  whistleblowers: SearchResult[]
  cases: SearchResult[]
  entities: SearchResult[]
}

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResults | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (query.length < 2) return

    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`)
      if (res.ok) {
        setResults(await res.json())
      }
    } catch (error) {
      console.error('Erreur:', error)
    } finally {
      setLoading(false)
    }
  }

  const totalResults = results 
    ? results.whistleblowers.length + results.cases.length + results.entities.length 
    : 0

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="bg-white border-b">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-3xl font-bold text-slate-900 text-center mb-8">Recherche</h1>
          
          <form onSubmit={handleSearch} className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-6 w-6 text-slate-400" />
            <input
              type="text"
              placeholder="Rechercher un lanceur d'alerte, une affaire..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full pl-14 pr-4 py-4 text-lg border-2 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
              autoFocus
            />
            <button
              type="submit"
              disabled={query.length < 2 || loading}
              className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 bg-amber-500 hover:bg-amber-600 disabled:bg-slate-300 text-white font-medium rounded-lg transition"
            >
              {loading ? '...' : 'Rechercher'}
            </button>
          </form>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {results && (
          <>
            <p className="text-slate-500 mb-6">
              {totalResults} résultat{totalResults > 1 ? 's' : ''} pour "{results.query}"
            </p>

            {results.whistleblowers.length > 0 && (
              <div className="mb-8">
                <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
                  <Users className="h-5 w-5 text-amber-500" />
                  Lanceurs d'alerte
                </h2>
                <div className="space-y-2">
                  {results.whistleblowers.map((r) => (
                    <Link
                      key={r.id}
                      to={`/lanceur/${r.slug}`}
                      className="block p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition border border-slate-100"
                    >
                      <span className="font-medium text-slate-900 hover:text-amber-600">{r.name}</span>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {results.cases.length > 0 && (
              <div className="mb-8">
                <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
                  <FileText className="h-5 w-5 text-amber-500" />
                  Affaires
                </h2>
                <div className="space-y-2">
                  {results.cases.map((r) => (
                    <Link
                      key={r.id}
                      to={`/affaire/${r.slug}`}
                      className="block p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition border border-slate-100"
                    >
                      <span className="font-medium text-slate-900 hover:text-amber-600">{r.name}</span>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {results.entities.length > 0 && (
              <div className="mb-8">
                <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
                  <Building2 className="h-5 w-5 text-slate-500" />
                  Entités
                </h2>
                <div className="space-y-2">
                  {results.entities.map((r) => (
                    <div
                      key={r.id}
                      className="p-4 bg-white rounded-lg shadow-sm border border-slate-100"
                    >
                      <span className="font-medium text-slate-900">{r.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {totalResults === 0 && (
              <div className="text-center py-12">
                <Search className="h-16 w-16 text-slate-300 mx-auto mb-4" />
                <p className="text-slate-600">Aucun résultat trouvé pour "{results.query}"</p>
              </div>
            )}
          </>
        )}

        {!results && (
          <div className="text-center py-12 text-slate-500">
            <p>Entrez au moins 2 caractères pour rechercher</p>
          </div>
        )}
      </div>
    </div>
  )
}
