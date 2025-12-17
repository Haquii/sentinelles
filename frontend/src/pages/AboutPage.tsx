import { Shield, Heart, Scale, BookOpen, ExternalLink } from 'lucide-react'

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
          <Shield className="h-16 w-16 text-amber-400 mx-auto mb-6" />
          <h1 className="text-4xl font-bold mb-4">À propos de Sentinelles</h1>
          <p className="text-xl text-slate-300">
            Une plateforme pour honorer ceux qui ont eu le courage de dire la vérité
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Notre mission</h2>
          <div className="prose prose-slate max-w-none">
            <p className="text-lg text-slate-600 leading-relaxed">
              Les lanceurs d'alerte sont souvent oubliés après les gros titres. Une fois le scandale passé, 
              ils restent seuls face aux conséquences de leur acte de courage : procès, exil, chômage, 
              parfois prison.
            </p>
            <p className="text-lg text-slate-600 leading-relaxed">
              <strong>Sentinelles</strong> existe pour préserver leur mémoire, documenter leurs histoires, 
              et rappeler que derrière chaque grande révélation, il y a des êtres humains qui ont tout risqué 
              pour nous informer.
            </p>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-slate-900 mb-6">Nos valeurs</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <Heart className="h-8 w-8 text-amber-500 mb-4" />
              <h3 className="font-semibold text-lg text-slate-900 mb-2">Mémoire</h3>
              <p className="text-slate-600">
                Préserver la mémoire de ceux qui ont sacrifié leur confort, leur carrière, 
                parfois leur liberté pour la vérité.
              </p>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <BookOpen className="h-8 w-8 text-amber-500 mb-4" />
              <h3 className="font-semibold text-lg text-slate-900 mb-2">Éducation</h3>
              <p className="text-slate-600">
                Aider à comprendre les enjeux des affaires révélées et leur impact 
                sur nos sociétés.
              </p>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <Scale className="h-8 w-8 text-amber-500 mb-4" />
              <h3 className="font-semibold text-lg text-slate-900 mb-2">Protection</h3>
              <p className="text-slate-600">
                Sensibiliser à l'importance de protéger légalement les lanceurs d'alerte 
                dans tous les pays.
              </p>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <Shield className="h-8 w-8 text-amber-500 mb-4" />
              <h3 className="font-semibold text-lg text-slate-900 mb-2">Transparence</h3>
              <p className="text-slate-600">
                Nous ne prétendons pas détenir la vérité absolue. Nous documentons et 
                indiquons toujours nos sources.
              </p>
            </div>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Un projet Declic.cloud</h2>
          <div className="bg-amber-50 rounded-xl p-6 border border-amber-100">
            <p className="text-slate-700 mb-4">
              <strong>Sentinelles</strong> fait partie de <strong>Declic.cloud</strong>, une plateforme 
              citoyenne française dédiée à la transparence. Notre mission : fournir aux citoyens des 
              outils gratuits pour s'informer de manière éclairée.
            </p>
            <a
              href="https://declic.cloud"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-amber-600 hover:text-amber-700 font-medium"
            >
              Découvrir Declic.cloud
              <ExternalLink className="ml-1 h-4 w-4" />
            </a>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Nos sources</h2>
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <p className="text-slate-600 mb-4">
              Toutes les informations présentes sur Sentinelles proviennent de sources publiques vérifiables :
            </p>
            <ul className="list-disc list-inside text-slate-600 space-y-2">
              <li>Articles de presse de médias reconnus (The Guardian, Le Monde, Washington Post...)</li>
              <li>Documents officiels et décisions de justice</li>
              <li>Témoignages publics des lanceurs d'alerte</li>
              <li>Rapports d'ONG (Amnesty International, Transparency International...)</li>
              <li>Documentaires et enquêtes journalistiques</li>
            </ul>
            <p className="text-slate-500 text-sm mt-4">
              Si vous constatez une erreur ou souhaitez suggérer une correction, 
              contactez-nous à contact@declic.cloud
            </p>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Nous soutenir</h2>
          <div className="bg-slate-900 text-white rounded-xl p-6">
            <p className="mb-4">
              Sentinelles est un projet bénévole, sans publicité et sans revente de données. 
              Si vous souhaitez nous aider à continuer :
            </p>
            <a
              href="https://buymeacoffee.com/haqumusic"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-6 py-3 bg-amber-500 hover:bg-amber-400 text-slate-900 font-semibold rounded-lg transition"
            >
              ☕ Offrir un café
            </a>
          </div>
        </section>
      </div>
    </div>
  )
}
