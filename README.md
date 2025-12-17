# Sentinelles 🛡️

> Une plateforme dédiée à la mémoire des lanceurs d'alerte

## Présentation

**Sentinelles** est une plateforme citoyenne qui documente et honore les lanceurs d'alerte du monde entier. Parce que leur courage mérite d'être préservé dans nos mémoires.

🔗 **Site** : [sentinelles.declic.cloud](https://sentinelles.declic.cloud)

## Fonctionnalités

- 📋 **Fiches lanceurs d'alerte** : Profils détaillés avec contexte, révélations, impact et conséquences personnelles
- 📰 **Fiches affaires** : Documentation des grandes affaires révélées (Pegasus, Cambridge Analytica, LuxLeaks...)
- 🔍 **Recherche** : Recherche globale par nom, domaine, statut
- 📚 **Ressources** : Articles, documentaires, livres pour approfondir

## Stack technique

### Backend (API)
- **FastAPI** - Framework Python
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de données

### Frontend
- **React 18** + **TypeScript**
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Routing
- **Lucide React** - Icons

### Infrastructure
- **Docker** - Containerisation
- **Traefik** - Reverse proxy
- **Cloudflare** - DNS & SSL

## Développement local

```bash
# Backend
cd api
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Un projet Declic.cloud

Sentinelles fait partie de [Declic.cloud](https://declic.cloud), une plateforme citoyenne française dédiée à la transparence.

### Autres outils Declic
- [EthiScan](https://ethiscan.declic.cloud) - Analyse éthique des marques
- [VisuPol](https://visupol.declic.cloud) - Transparence politique

## Nous soutenir

Ce projet est bénévole, sans publicité et sans revente de données.

☕ [Offrir un café](https://buymeacoffee.com/haqumusic)

## Licence

MIT

---

*Fait avec ❤️ par des citoyens engagés*
