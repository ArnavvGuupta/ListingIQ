
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Listing
from schemas import BulkListingRequest, ListingResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Business Listings Dashboard API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def health_check():
    return {"status": "ok", "message": "Business Listings API is running"}


@app.post("/api/listings/bulk")
def bulk_insert(
    payload: BulkListingRequest,
    db: Session = Depends(get_db),
):
    try:
        records = [
            Listing(**item.model_dump())
            for item in payload.listings
        ]

        db.add_all(records)
        db.commit()

        return {
            "inserted": len(records),
            "message": "Listings inserted successfully",
        }
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database insert failed. Check the backend logs.",
        )


@app.get("/api/listings", response_model=list[ListingResponse])
def get_listings(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return (
        db.query(Listing)
        .order_by(Listing.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )



@app.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    sample = (
        db.query(Listing)
        .order_by(Listing.id.desc())
        .limit(500)
        .subquery()
    )

    return {
        "total_listings": db.query(sample).count(),
        "cities": db.query(sample.c.city).distinct().count(),
        "categories": (
            db.query(sample.c.category)
            .filter(sample.c.category.isnot(None))
            .distinct()
            .count()
        ),
        "sources": db.query(sample.c.source).distinct().count(),
    }



def dashboard_base_query(db: Session, limit: int | None):
    """Build a consistent listing query, optionally limited to recent records."""
    query = db.query(Listing)

    if limit is not None:
        query = query.order_by(Listing.id.desc()).limit(limit).subquery()
        return query

    return query.subquery()


def get_counts(db: Session, field_name: str, limit: int | None):
    base = dashboard_base_query(db, limit)

    column = getattr(base.c, field_name)

    rows = (
        db.query(
            column.label("name"),
            func.count().label("count"),
        )
        .filter(column.isnot(None))
        .group_by(column)
        .order_by(func.count().desc())
        .all()
    )

    return [
        {"name": name, "count": count}
        for name, count in rows
    ]


@app.get("/api/dashboard/cities")
def city_counts(
    limit: int | None = Query(default=500, ge=1, le=100000),
    db: Session = Depends(get_db),
):
    return get_counts(db, "city", limit)


@app.get("/api/dashboard/categories")
def category_counts(
    limit: int | None = Query(default=500, ge=1, le=100000),
    db: Session = Depends(get_db),
):
    return get_counts(db, "category", limit)


@app.get("/api/dashboard/sources")
def source_counts(
    limit: int | None = Query(default=500, ge=1, le=100000),
    db: Session = Depends(get_db),
):
    return get_counts(db, "source", limit)
