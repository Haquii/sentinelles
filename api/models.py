"""
Sentinelles - Modèles de données
Lanceurs d'alerte & Affaires majeures
"""

from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


# ==================== ENUMS ====================

class WhistleblowerStatus(str, enum.Enum):
    """Statut actuel du lanceur d'alerte"""
    LIBRE = "libre"
    EXILE = "exilé"
    EMPRISONNE = "emprisonné"
    EN_PROCES = "en procès"
    REHABILITE = "réhabilité"
    DECEDE = "décédé"
    ANONYME = "anonyme"
    INCONNU = "inconnu"


class CaseStatus(str, enum.Enum):
    """Statut d'une affaire"""
    EN_COURS = "en cours"
    RESOLU = "résolu"
    IMPUNI = "impuni"
    PARTIELLEMENT_RESOLU = "partiellement résolu"


class Domain(str, enum.Enum):
    """Domaines des révélations"""
    FINANCE = "finance"
    ENVIRONNEMENT = "environnement"
    SANTE = "santé"
    SURVEILLANCE = "surveillance"
    DEFENSE = "défense"
    CORRUPTION = "corruption"
    DROITS_HUMAINS = "droits humains"
    FISCALITE = "fiscalité"
    NUCLEAIRE = "nucléaire"
    AGROALIMENTAIRE = "agroalimentaire"
    PHARMACEUTIQUE = "pharmaceutique"
    TECHNOLOGIE = "technologie"
    POLITIQUE = "politique"
    AUTRE = "autre"


class ResourceType(str, enum.Enum):
    """Types de ressources"""
    ARTICLE = "article"
    LIVRE = "livre"
    DOCUMENTAIRE = "documentaire"
    FILM = "film"
    SERIE = "série"
    PODCAST = "podcast"
    SITE_OFFICIEL = "site officiel"
    WIKIPEDIA = "wikipedia"
    INTERVIEW = "interview"
    JUGEMENT = "jugement"


class RevealerType(str, enum.Enum):
    """Type de révélateur pour une affaire"""
    LANCEUR_ALERTE = "lanceur d'alerte"
    JOURNALISTE = "journaliste"
    MEDIA = "média"
    ONG = "ONG"
    ENQUETE_COLLABORATIVE = "enquête collaborative"
    FUITE_ANONYME = "fuite anonyme"
    CHERCHEUR = "chercheur"
    AUTORITE = "autorité"


# ==================== TABLES D'ASSOCIATION ====================

whistleblower_cases = Table(
    'whistleblower_cases',
    Base.metadata,
    Column('whistleblower_id', Integer, ForeignKey('whistleblowers.id'), primary_key=True),
    Column('case_id', Integer, ForeignKey('cases.id'), primary_key=True)
)

case_entities = Table(
    'case_entities',
    Base.metadata,
    Column('case_id', Integer, ForeignKey('cases.id'), primary_key=True),
    Column('entity_id', Integer, ForeignKey('entities.id'), primary_key=True)
)


# ==================== MODÈLES PRINCIPAUX ====================

class Whistleblower(Base):
    """Lanceur d'alerte (personne)"""
    __tablename__ = 'whistleblowers'

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(200), unique=True, index=True)
    
    name = Column(String(200), nullable=False, index=True)
    photo_url = Column(String(500), nullable=True)
    nationality = Column(String(100), nullable=True)
    birth_year = Column(Integer, nullable=True)
    profession = Column(String(200), nullable=True)
    
    main_revelation = Column(String(300), nullable=True)
    revelation_year = Column(Integer, nullable=True)
    
    summary = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    stakes = Column(Text, nullable=True)
    impact = Column(Text, nullable=True)
    
    status = Column(String(50), default=WhistleblowerStatus.INCONNU.value)
    refuge_country = Column(String(100), nullable=True)
    personal_consequences = Column(Text, nullable=True)
    
    is_protected = Column(Boolean, default=False)
    awards = Column(Text, nullable=True)
    
    quote = Column(Text, nullable=True)
    quote_source = Column(String(200), nullable=True)
    
    is_featured = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    resources = relationship("Resource", back_populates="whistleblower", cascade="all, delete-orphan",
                            foreign_keys="Resource.whistleblower_id")
    domain_tags = relationship("DomainTag", back_populates="whistleblower", cascade="all, delete-orphan",
                              foreign_keys="DomainTag.whistleblower_id")
    cases = relationship("Case", secondary=whistleblower_cases, back_populates="whistleblowers")


class Case(Base):
    """Affaire majeure (révélation/scandale)"""
    __tablename__ = 'cases'
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(200), unique=True, index=True)
    
    name = Column(String(300), nullable=False, index=True)
    short_name = Column(String(100), nullable=True)
    image_url = Column(String(500), nullable=True)
    
    domain = Column(String(50), nullable=False)
    
    revelation_date = Column(Date, nullable=True)
    revelation_year = Column(Integer, nullable=False)
    period_start = Column(Integer, nullable=True)
    period_end = Column(Integer, nullable=True)
    
    summary = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    revelations = Column(Text, nullable=True)
    
    scope = Column(Text, nullable=True)
    countries_involved = Column(String(500), nullable=True)
    
    revealed_by = Column(Text, nullable=True)
    revealer_type = Column(String(50), nullable=True)
    key_journalists = Column(Text, nullable=True)
    key_organizations = Column(Text, nullable=True)
    
    legal_consequences = Column(Text, nullable=True)
    legislative_changes = Column(Text, nullable=True)
    public_impact = Column(Text, nullable=True)
    
    status = Column(String(50), default=CaseStatus.EN_COURS.value)
    status_details = Column(Text, nullable=True)
    
    is_featured = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    whistleblowers = relationship("Whistleblower", secondary=whistleblower_cases, back_populates="cases")
    entities = relationship("Entity", secondary=case_entities, back_populates="cases")
    resources = relationship("Resource", back_populates="case", cascade="all, delete-orphan",
                            foreign_keys="Resource.case_id")
    domain_tags = relationship("DomainTag", back_populates="case", cascade="all, delete-orphan",
                              foreign_keys="DomainTag.case_id")


class Entity(Base):
    """Entités impliquées"""
    __tablename__ = 'entities'
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(200), unique=True, index=True)
    
    name = Column(String(200), nullable=False, index=True)
    entity_type = Column(String(50), nullable=True)
    country = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    
    cases = relationship("Case", secondary=case_entities, back_populates="entities")


class Resource(Base):
    """Ressources pour en savoir plus"""
    __tablename__ = 'resources'
    
    id = Column(Integer, primary_key=True, index=True)
    
    whistleblower_id = Column(Integer, ForeignKey('whistleblowers.id'), nullable=True)
    case_id = Column(Integer, ForeignKey('cases.id'), nullable=True)
    
    resource_type = Column(String(50), nullable=False)
    title = Column(String(300), nullable=False)
    url = Column(String(500), nullable=True)
    author = Column(String(200), nullable=True)
    publisher = Column(String(200), nullable=True)
    year = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    is_primary = Column(Boolean, default=False)
    is_free = Column(Boolean, default=True)
    language = Column(String(10), default="fr")
    
    whistleblower = relationship("Whistleblower", back_populates="resources", foreign_keys=[whistleblower_id])
    case = relationship("Case", back_populates="resources", foreign_keys=[case_id])


class DomainTag(Base):
    """Tags de domaines"""
    __tablename__ = 'domain_tags'
    
    id = Column(Integer, primary_key=True, index=True)
    
    whistleblower_id = Column(Integer, ForeignKey('whistleblowers.id'), nullable=True)
    case_id = Column(Integer, ForeignKey('cases.id'), nullable=True)
    
    domain = Column(String(50), nullable=False)
    
    whistleblower = relationship("Whistleblower", back_populates="domain_tags", foreign_keys=[whistleblower_id])
    case = relationship("Case", back_populates="domain_tags", foreign_keys=[case_id])


class Timeline(Base):
    """Événements clés"""
    __tablename__ = 'timeline_events'
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('cases.id'), nullable=False)
    
    event_date = Column(Date, nullable=True)
    event_year = Column(Integer, nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    source_url = Column(String(500), nullable=True)
    
    case = relationship("Case")
