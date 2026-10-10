from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Tender

router = APIRouter(
    prefix="/tenders",
    tags=["Tenders"]
)

@router.post("/")
def create_tender(
    title: str,
    description: str,
    starting_price: float,
    db: Session = Depends(get_db)
):
    tender = Tender(
        title=title,
        description=description,
        starting_price=starting_price
    )

    db.add(tender)
    db.commit()
    db.refresh(tender)

    return {
        "message": "Tender created successfully",
        "tender_id": tender.id,
        "title": tender.title,
        "starting_price": tender.starting_price,
        "status": tender.status
    }

@router.get("/")
def get_tenders(db: Session = Depends(get_db)):
    tenders = db.query(Tender).all()

    return tenders


@router.get("/{tender_id}")
def get_tender(
    tender_id: int,
    db: Session = Depends(get_db)
):
    tender = db.query(Tender).filter(
        Tender.id == tender_id
    ).first()

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )

    return tender