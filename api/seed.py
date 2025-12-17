"""
Sentinelles - Script de seed pour données initiales
Lanceurs d'alerte & Affaires emblématiques
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from models import (
    Base, Whistleblower, Case, Resource, DomainTag, Entity,
    WhistleblowerStatus, CaseStatus
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://declic:password@declic-postgres:5432/declic")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def slugify(text):
    import re
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def seed_data():
    db = SessionLocal()
    
    try:
        existing = db.query(Whistleblower).first()
        if existing:
            print("Des données existent déjà. Abandon.")
            return
        
        print("🌱 Création des données initiales...")
        
        # ENTITÉS
        entities = {
            "nsa": Entity(slug="nsa", name="NSA (National Security Agency)", entity_type="agence", country="États-Unis"),
            "nso": Entity(slug="nso-group", name="NSO Group", entity_type="entreprise", country="Israël"),
            "pwc": Entity(slug="pwc", name="PwC (PricewaterhouseCoopers)", entity_type="entreprise", country="International"),
            "hsbc": Entity(slug="hsbc", name="HSBC", entity_type="entreprise", country="Royaume-Uni"),
            "ubs": Entity(slug="ubs", name="UBS", entity_type="entreprise", country="Suisse"),
            "servier": Entity(slug="servier", name="Laboratoires Servier", entity_type="entreprise", country="France"),
            "facebook": Entity(slug="facebook-meta", name="Facebook/Meta", entity_type="entreprise", country="États-Unis"),
            "cambridge": Entity(slug="cambridge-analytica", name="Cambridge Analytica", entity_type="entreprise", country="Royaume-Uni"),
            "palantir": Entity(slug="palantir", name="Palantir Technologies", entity_type="entreprise", country="États-Unis")
        }
        
        for entity in entities.values():
            db.add(entity)
        db.flush()
        
        # AFFAIRES
        pegasus = Case(
            slug="projet-pegasus", name="Projet Pegasus", short_name="Pegasus", domain="surveillance",
            revelation_year=2021, period_start=2016,
            summary="Révélation de l'utilisation massive du logiciel espion Pegasus par des gouvernements pour surveiller journalistes et militants.",
            revealed_by="Forbidden Stories, Amnesty International et 17 médias internationaux",
            revealer_type="enquête collaborative",
            status=CaseStatus.EN_COURS.value, is_featured=True, is_verified=True
        )
        pegasus.entities.append(entities["nso"])
        db.add(pegasus)
        
        cambridge_case = Case(
            slug="cambridge-analytica", name="Scandale Cambridge Analytica", short_name="Cambridge Analytica",
            domain="technologie", revelation_year=2018, period_start=2014, period_end=2018,
            summary="Exploitation illégale des données de 87 millions d'utilisateurs Facebook pour influencer des élections.",
            revealed_by="Christopher Wylie", revealer_type="lanceur d'alerte",
            status=CaseStatus.PARTIELLEMENT_RESOLU.value, is_featured=True, is_verified=True
        )
        cambridge_case.entities.extend([entities["facebook"], entities["cambridge"], entities["palantir"]])
        db.add(cambridge_case)
        
        prism = Case(
            slug="nsa-prism", name="Révélations sur la surveillance de masse de la NSA", short_name="NSA/PRISM",
            domain="surveillance", revelation_year=2013, period_start=2007,
            summary="Révélation des programmes de surveillance de masse de la NSA collectant les données de millions de citoyens.",
            revealed_by="Edward Snowden", revealer_type="lanceur d'alerte",
            status=CaseStatus.PARTIELLEMENT_RESOLU.value, is_featured=True, is_verified=True
        )
        prism.entities.append(entities["nsa"])
        db.add(prism)
        
        luxleaks = Case(
            slug="luxleaks", name="LuxLeaks", short_name="LuxLeaks", domain="fiscalité",
            revelation_year=2014, period_start=2002, period_end=2010,
            summary="Révélation d'accords fiscaux secrets entre le Luxembourg et des multinationales.",
            revealed_by="Antoine Deltour et Raphaël Halet", revealer_type="lanceur d'alerte",
            status=CaseStatus.PARTIELLEMENT_RESOLU.value, is_featured=True, is_verified=True
        )
        luxleaks.entities.append(entities["pwc"])
        db.add(luxleaks)
        
        db.flush()
        
        # LANCEURS D'ALERTE
        snowden = Whistleblower(
            slug="edward-snowden", name="Edward Snowden", nationality="Américaine", birth_year=1983,
            profession="Analyste NSA / Consultant CIA", main_revelation="Surveillance de masse de la NSA",
            revelation_year=2013,
            summary="A révélé l'ampleur de la surveillance de masse pratiquée par la NSA.",
            status=WhistleblowerStatus.EXILE.value, refuge_country="Russie",
            quote="Affirmer que vous ne vous souciez pas du droit à la vie privée parce que vous n'avez rien à cacher revient à dire que vous ne vous souciez pas de la liberté d'expression parce que vous n'avez rien à dire.",
            is_featured=True, is_verified=True
        )
        snowden.cases.append(prism)
        db.add(snowden)
        
        deltour = Whistleblower(
            slug="antoine-deltour", name="Antoine Deltour", nationality="Française", birth_year=1985,
            profession="Auditeur chez PwC Luxembourg", main_revelation="LuxLeaks - Évasion fiscale",
            revelation_year=2014,
            summary="A révélé 28 000 pages de documents exposant les accords fiscaux secrets du Luxembourg.",
            status=WhistleblowerStatus.REHABILITE.value,
            is_featured=True, is_verified=True
        )
        deltour.cases.append(luxleaks)
        db.add(deltour)
        
        wylie = Whistleblower(
            slug="christopher-wylie", name="Christopher Wylie", nationality="Canadienne", birth_year=1989,
            profession="Directeur de recherche chez Cambridge Analytica", main_revelation="Cambridge Analytica",
            revelation_year=2018,
            summary="A révélé comment Cambridge Analytica a exploité les données de 87 millions d'utilisateurs Facebook.",
            status=WhistleblowerStatus.LIBRE.value,
            is_featured=True, is_verified=True
        )
        wylie.cases.append(cambridge_case)
        db.add(wylie)
        
        haugen = Whistleblower(
            slug="frances-haugen", name="Frances Haugen", nationality="Américaine", birth_year=1983,
            profession="Ingénieure chez Facebook", main_revelation="Facebook Papers",
            revelation_year=2021,
            summary="A révélé que Facebook savait que ses algorithmes causaient des dommages psychologiques.",
            status=WhistleblowerStatus.LIBRE.value,
            is_featured=True, is_verified=True
        )
        db.add(haugen)
        
        frachon = Whistleblower(
            slug="irene-frachon", name="Irène Frachon", nationality="Française", birth_year=1963,
            profession="Pneumologue au CHU de Brest", main_revelation="Scandale du Mediator",
            revelation_year=2010,
            summary="A révélé que le Mediator était responsable de centaines de morts.",
            status=WhistleblowerStatus.LIBRE.value,
            is_featured=True, is_verified=True
        )
        db.add(frachon)
        
        falciani = Whistleblower(
            slug="herve-falciani", name="Hervé Falciani", nationality="Franco-italienne", birth_year=1972,
            profession="Informaticien chez HSBC Genève", main_revelation="SwissLeaks - Évasion fiscale HSBC",
            revelation_year=2008,
            summary="A fourni aux autorités une liste de 130 000 évadés fiscaux chez HSBC Suisse.",
            status=WhistleblowerStatus.EN_PROCES.value,
            is_featured=True, is_verified=True
        )
        db.add(falciani)
        
        gibaud = Whistleblower(
            slug="stephanie-gibaud", name="Stéphanie Gibaud", nationality="Française", birth_year=1966,
            profession="Responsable marketing chez UBS France", main_revelation="Fraude fiscale UBS",
            revelation_year=2008,
            summary="A révélé le système de démarchage illégal de clients français par UBS.",
            status=WhistleblowerStatus.LIBRE.value,
            is_featured=True, is_verified=True
        )
        db.add(gibaud)
        
        assange = Whistleblower(
            slug="julian-assange", name="Julian Assange", nationality="Australienne", birth_year=1971,
            profession="Fondateur de WikiLeaks", main_revelation="WikiLeaks - Documents militaires",
            revelation_year=2010,
            summary="A publié via WikiLeaks des documents secrets révélant des crimes de guerre.",
            status=WhistleblowerStatus.LIBRE.value,
            is_featured=True, is_verified=True
        )
        db.add(assange)
        
        manning = Whistleblower(
            slug="chelsea-manning", name="Chelsea Manning", nationality="Américaine", birth_year=1987,
            profession="Analyste du renseignement militaire US", main_revelation="Documents militaires US",
            revelation_year=2010,
            summary="A transmis à WikiLeaks 750 000 documents révélant des crimes de guerre.",
            status=WhistleblowerStatus.LIBRE.value,
            is_featured=True, is_verified=True
        )
        db.add(manning)
        
        db.commit()
        print("✅ Données créées avec succès !")
        add_domain_tags(db)
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        db.rollback()
        raise
    finally:
        db.close()


def add_domain_tags(db):
    tags = [
        ("edward-snowden", ["surveillance", "défense"]),
        ("antoine-deltour", ["fiscalité", "finance"]),
        ("christopher-wylie", ["technologie", "politique"]),
        ("frances-haugen", ["technologie"]),
        ("irene-frachon", ["santé", "pharmaceutique"]),
        ("herve-falciani", ["fiscalité", "finance"]),
        ("stephanie-gibaud", ["fiscalité", "finance"]),
        ("julian-assange", ["défense", "politique"]),
        ("chelsea-manning", ["défense"]),
    ]
    
    for slug, domains in tags:
        wb = db.query(Whistleblower).filter(Whistleblower.slug == slug).first()
        if wb:
            for domain in domains:
                db.add(DomainTag(whistleblower_id=wb.id, domain=domain))
    
    case_tags = [
        ("projet-pegasus", ["surveillance", "droits humains"]),
        ("cambridge-analytica", ["technologie", "politique"]),
        ("nsa-prism", ["surveillance"]),
        ("luxleaks", ["fiscalité"]),
    ]
    
    for slug, domains in case_tags:
        case = db.query(Case).filter(Case.slug == slug).first()
        if case:
            for domain in domains:
                db.add(DomainTag(case_id=case.id, domain=domain))
    
    db.commit()
    print("   - Tags de domaines ajoutés")


if __name__ == "__main__":
    print("🚀 Lancement du seed Sentinelles...")
    seed_data()
