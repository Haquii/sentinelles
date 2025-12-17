import { Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import WhistleblowersPage from './pages/WhistleblowersPage'
import WhistleblowerPage from './pages/WhistleblowerPage'
import CasesPage from './pages/CasesPage'
import CasePage from './pages/CasePage'
import AboutPage from './pages/AboutPage'
import SearchPage from './pages/SearchPage'

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <Header />
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/lanceurs" element={<WhistleblowersPage />} />
          <Route path="/lanceur/:slug" element={<WhistleblowerPage />} />
          <Route path="/affaires" element={<CasesPage />} />
          <Route path="/affaire/:slug" element={<CasePage />} />
          <Route path="/recherche" element={<SearchPage />} />
          <Route path="/a-propos" element={<AboutPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default App