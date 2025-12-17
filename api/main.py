"""
Sentinelles API - Lanceurs d'alerte & Affaires
API FastAPI pour la plateforme Declic.cloud
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, or_, func
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import os

from models import (
    Base, Whistleblower, Case, Resource, DomainTag, Entity, Timeline,
    WhistleblowerStatus, CaseStatus, Domain
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://declic:password@declic-postgres:5432/declic")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sentinelles API",
    description="API pour les lanceurs d'alerte et affaires majeures - Plateforme Declic.cloud",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sentinelles.declic.cloud",
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== SCHEMAS ====================

class ResourceSchema(BaseModel):
    id: int
    resource_type: str
    title: str
    url: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    is_primary: bool
    is_free: bool
    language: str

    class Config:
        from_attributes = True


class EntitySchema(BaseModel):
    id: int
    slug: str
    name: str
    entity_type: Optional[str] = None
    country: Optional[str] = None
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True


class WhistleblowerListSchema(BaseModel):
    id: int
    slug: str
    name: str
    photo_url: Optional[str] = None
    nationality: Optional[str] = None
    main_revelation: Optional[str] = None
    revelation_year: Optional[int] = None
    status: str
    domains: List[str]
    summary: str
    is_featured: bool

    class Config:
        from_attributes = True


class WhistleblowerDetailSchema(BaseModel):
    id: int
    slug: str
    name: str
    photo_url: Optional[str] = None
    nationality: Optional[str] = None
    birth_year: Optional[int] = None
    profession: Optional[str] = None
    main_revelation: Optional[str] = None
    revelation_year: Optional[int] = None
    summary: str
    context: Optional[str] = None
    stakes: Optional[str] = None
    impact: Optional[str] = None
    status: str
    refuge_country: Optional[str] = None
    personal_consequences: Optional[str] = None
    is_protected: bool
    awards: Optional[str] = None
    quote: Optional[str] = None
    quote_source: Optional[str] = None
    domains: List[str]
    resources: List[ResourceSchema]
    related_cases: List[dict]
    is_featured: bool
    is_verified: bool

    class Config:
        from_attributes = True


class CaseListSchema(BaseModel):
    id: int
    slug: str
    name: str
    short_name: Optional[str] = None
    image_url: Optional[str] = None
    domain: str
    revelation_year: int
    summary: str
    revealer_type: Optional[str] = None
    status: str
    domains: List[str]
    is_featured: bool

    class Config:
        from_attributes = True


class CaseDetailSchema(BaseModel):
    id: int
    slug: str
    name: str
    short_name: Optional[str] = None
    image_url: Optional[str] = None
    domain: str
    revelation_date: Optional[date] = None
    revelation_year: int
    period_start: Optional[int] = None
    period_end: Optional[int] = None
    summary: str
    context: Optional[str] = None
    revelations: Optional[str] = None
    scope: Optional[str] = None
    countries_involved: Optional[str] = None
    revealed_by: Optional[str] = None
    revealer_type: Optional[str] = None
    key_journalists: Optional[str] = None
    key_organizations: Optional[str] = None
    legal_consequences: Optional[str] = None
    legislative_changes: Optional[str] = None
    public_impact: Optional[str] = None
    status: str
    status_details: Optional[str] = None
    domains: List[str]
    resources: List[ResourceSchema]
    whistleblowers: List[dict]
    entities: List[EntitySchema]
    is_featured: bool
    is_verified: bool

    class Config:
        from_attributes = True


class StatsSchema(BaseModel):
    total_whistleblowers: int
    total_cases: int
    whistleblowers_by_status: dict
    cases_by_domain: dict
    featured_whistleblowers: int
    featured_cases: int


# ==================== ROUTES ====================

@app.get("/")
def root():
    return {
        "service": "Sentinelles API",
        "version": "2.0.0",
        "description": "Hommage aux lanceurs d'alerte",
        "project": "Declic.cloud"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/stats", response_model=StatsSchema)
def get_stats(db: Session = Depends(get_db)):
    total_wb = db.query(Whistleblower).filter(Whistleblower.is_verified == True).count()
    total_cases = db.query(Case).filter(Case.is_verified == True).count()
    
    featured_wb = db.query(Whistleblower).filter(
        Whistleblower.is_verified == True,
        Whistleblower.is_featured == True
    ).count()
    
    featured_cases = db.query(Case).filter(
        Case.is_verified == True,
        Case.is_featured == True
    ).count()
    
    wb_statuses = db.query(
        Whistleblower.status,
        func.count(Whistleblower.id)
    ).filter(Whistleblower.is_verified == True).group_by(Whistleblower.status).all()
    
    case_domains = db.query(
        Case.domain,
        func.count(Case.id)
    ).filter(Case.is_verified == True).group_by(Case.domain).all()
    
    return {
        "total_whistleblowers": total_wb,
        "total_cases": total_cases,
        "whistleblowers_by_status": {s[0]: s[1] for s in wb_statuses},
        "cases_by_domain": {d[0]: d[1] for d in case_domains},
        "featured_whistleblowers": featured_wb,
        "featured_cases": featured_cases
    }


@app.get("/domains")
def list_domains(db: Session = Depends(get_db)):
    wb_domains = db.query(
        DomainTag.domain,
        func.count(DomainTag.whistleblower_id).label('count')
    ).filter(DomainTag.whistleblower_id.isnot(None)).group_by(DomainTag.domain).all()
    
    case_domains = db.query(
        Case.domain,
        func.count(Case.id).label('count')
    ).filter(Case.is_verified == True).group_by(Case.domain).all()
    
    all_domains = {}
    for d in wb_domains:
        all_domains[d[0]] = {"whistleblowers": d[1], "cases": 0}
    for d in case_domains:
        if d[0] in all_domains:
            all_domains[d[0]]["cases"] = d[1]
        else:
            all_domains[d[0]] = {"whistleblowers": 0, "cases": d[1]}
    
    return [{"domain": k, **v} for k, v in all_domains.items()]


@app.get("/whistleblowers", response_model=List[WhistleblowerListSchema])
def list_whistleblowers(
    domain: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    featured_only: bool = False,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Whistleblower).filter(Whistleblower.is_verified == True)
    
    if featured_only:
        query = query.filter(Whistleblower.is_featured == True)
    if status:
        query = query.filter(Whistleblower.status == status)
    if search:
        query = query.filter(or_(
            Whistleblower.name.ilike(f"%{search}%"),
            Whistleblower.main_revelation.ilike(f"%{search}%")
        ))
    if domain:
        query = query.join(DomainTag).filter(DomainTag.domain == domain)
    
    query = query.order_by(Whistleblower.is_featured.desc(), Whistleblower.revelation_year.desc().nullslast())
    whistleblowers = query.offset(offset).limit(limit).all()
    
    result = []
    for wb in whistleblowers:
        domains = db.query(DomainTag.domain).filter(DomainTag.whistleblower_id == wb.id).all()
        result.append({
            **{k: v for k, v in wb.__dict__.items() if not k.startswith('_')},
            "summary": wb.summary[:300] + "..." if len(wb.summary) > 300 else wb.summary,
            "domains": [d[0] for d in domains]
        })
    return result


@app.get("/whistleblowers/{identifier}", response_model=WhistleblowerDetailSchema)
def get_whistleblower(identifier: str, db: Session = Depends(get_db)):
    if identifier.isdigit():
        wb = db.query(Whistleblower).filter(Whistleblower.id == int(identifier), Whistleblower.is_verified == True).first()
    else:
        wb = db.query(Whistleblower).filter(Whistleblower.slug == identifier, Whistleblower.is_verified == True).first()
    
    if not wb:
        raise HTTPException(status_code=404, detail="Lanceur d'alerte non trouvé")
    
    domains = db.query(DomainTag.domain).filter(DomainTag.whistleblower_id == wb.id).all()
    resources = db.query(Resource).filter(Resource.whistleblower_id == wb.id).all()
    related_cases = [{"id": c.id, "slug": c.slug, "name": c.name, "revelation_year": c.revelation_year} for c in wb.cases]
    
    return {
        **{k: v for k, v in wb.__dict__.items() if not k.startswith('_')},
        "domains": [d[0] for d in domains],
        "resources": resources,
        "related_cases": related_cases
    }


@app.get("/cases", response_model=List[CaseListSchema])
def list_cases(
    domain: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    featured_only: bool = False,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Case).filter(Case.is_verified == True)
    
    if featured_only:
        query = query.filter(Case.is_featured == True)
    if domain:
        query = query.filter(Case.domain == domain)
    if status:
        query = query.filter(Case.status == status)
    if search:
        query = query.filter(or_(Case.name.ilike(f"%{search}%"), Case.summary.ilike(f"%{search}%")))
    
    query = query.order_by(Case.is_featured.desc(), Case.revelation_year.desc())
    cases = query.offset(offset).limit(limit).all()
    
    result = []
    for case in cases:
        domains = db.query(DomainTag.domain).filter(DomainTag.case_id == case.id).all()
        result.append({
            **{k: v for k, v in case.__dict__.items() if not k.startswith('_')},
            "summary": case.summary[:300] + "..." if len(case.summary) > 300 else case.summary,
            "domains": [d[0] for d in domains]
        })
    return result


@app.get("/cases/{identifier}", response_model=CaseDetailSchema)
def get_case(identifier: str, db: Session = Depends(get_db)):
    if identifier.isdigit():
        case = db.query(Case).filter(Case.id == int(identifier), Case.is_verified == True).first()
    else:
        case = db.query(Case).filter(Case.slug == identifier, Case.is_verified == True).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Affaire non trouvée")
    
    domains = db.query(DomainTag.domain).filter(DomainTag.case_id == case.id).all()
    resources = db.query(Resource).filter(Resource.case_id == case.id).all()
    whistleblowers = [{"id": wb.id, "slug": wb.slug, "name": wb.name, "photo_url": wb.photo_url, "status": wb.status} for wb in case.whistleblowers]
    
    return {
        **{k: v for k, v in case.__dict__.items() if not k.startswith('_')},
        "domains": [d[0] for d in domains],
        "resources": resources,
        "whistleblowers": whistleblowers,
        "entities": case.entities
    }


@app.get("/entities")
def list_entities(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Entity)
    if search:
        query = query.filter(Entity.name.ilike(f"%{search}%"))
    return [{"id": e.id, "slug": e.slug, "name": e.name, "entity_type": e.entity_type, "country": e.country, "cases_count": len(e.cases)} for e in query.all()]


@app.get("/entities/{identifier}")
def get_entity(identifier: str, db: Session = Depends(get_db)):
    if identifier.isdigit():
        entity = db.query(Entity).filter(Entity.id == int(identifier)).first()
    else:
        entity = db.query(Entity).filter(Entity.slug == identifier).first()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entité non trouvée")
    
    return {
        "id": entity.id,
        "slug": entity.slug,
        "name": entity.name,
        "entity_type": entity.entity_type,
        "country": entity.country,
        "description": entity.description,
        "logo_url": entity.logo_url,
        "cases": [{"id": c.id, "slug": c.slug, "name": c.name, "revelation_year": c.revelation_year} for c in entity.cases]
    }


@app.get("/search")
def global_search(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    whistleblowers = db.query(Whistleblower).filter(
        Whistleblower.is_verified == True,
        or_(Whistleblower.name.ilike(f"%{q}%"), Whistleblower.main_revelation.ilike(f"%{q}%"))
    ).limit(10).all()
    
    cases = db.query(Case).filter(
        Case.is_verified == True,
        or_(Case.name.ilike(f"%{q}%"), Case.summary.ilike(f"%{q}%"))
    ).limit(10).all()
    
    entities = db.query(Entity).filter(Entity.name.ilike(f"%{q}%")).limit(5).all()
    
    return {
        "query": q,
        "whistleblowers": [{"id": wb.id, "slug": wb.slug, "name": wb.name, "type": "whistleblower"} for wb in whistleblowers],
        "cases": [{"id": c.id, "slug": c.slug, "name": c.name, "type": "case"} for c in cases],
        "entities": [{"id": e.id, "slug": e.slug, "name": e.name, "type": "entity"} for e in entities]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
