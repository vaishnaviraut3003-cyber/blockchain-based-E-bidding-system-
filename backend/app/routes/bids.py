from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Bid, Tender, User
from ..blockchain import store_bid_hash, get_bid_hash

import hashlib
import json
from datetime import datetime


router = APIRouter(
    prefix="/bids",
    tags=["Bids"]
)


# ============================================================
# CREATE BID
# ============================================================

@router.post("/")
def create_bid(
    amount: float,
    bidder_id: int,
    tender_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # 1. Check whether bidder exists
    # --------------------------------------------------------

    bidder = db.query(User).filter(
        User.id == bidder_id
    ).first()

    if not bidder:
        raise HTTPException(
            status_code=404,
            detail="Bidder not found"
        )


    # --------------------------------------------------------
    # 2. Check whether tender exists
    # --------------------------------------------------------

    tender = db.query(Tender).filter(
        Tender.id == tender_id
    ).first()

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )


    # --------------------------------------------------------
    # 3. Check whether tender is open
    # --------------------------------------------------------

    if tender.status != "open":
        raise HTTPException(
            status_code=400,
            detail="Tender is closed"
        )


    # --------------------------------------------------------
    # 4. Check minimum bid
    # --------------------------------------------------------

    if amount < tender.starting_price:
        raise HTTPException(
            status_code=400,
            detail="Bid amount must be greater than or equal to starting price"
        )


    # --------------------------------------------------------
    # 5. Create timestamp
    # --------------------------------------------------------

    created_at = datetime.utcnow()


    # --------------------------------------------------------
    # 6. Prepare bid data for SHA-256
    # --------------------------------------------------------

    bid_data = {
        "amount": amount,
        "bidder_id": bidder_id,
        "tender_id": tender_id,
        "created_at": created_at.isoformat()
    }


    # --------------------------------------------------------
    # 7. Convert to consistent string
    # --------------------------------------------------------

    bid_string = json.dumps(
        bid_data,
        sort_keys=True
    )


    # --------------------------------------------------------
    # 8. Generate SHA-256 hash
    # --------------------------------------------------------

    bid_hash = hashlib.sha256(
        bid_string.encode("utf-8")
    ).hexdigest()


    print("\n====================================")
    print("          BID HASH GENERATED")
    print("====================================")
    print("Bid Hash:", bid_hash)


    # --------------------------------------------------------
    # 9. Create bid in SQLite
    # --------------------------------------------------------

    bid = Bid(
        amount=amount,
        bidder_id=bidder_id,
        tender_id=tender_id,
        created_at=created_at,
        bid_hash=bid_hash
    )


    # --------------------------------------------------------
    # 10. Save bid to SQLite
    # --------------------------------------------------------

    db.add(bid)
    db.commit()
    db.refresh(bid)


    print("Bid ID:", bid.id)
    print("✅ Bid saved in SQLite")


    # --------------------------------------------------------
    # 11. Store SHA-256 hash on blockchain
    # --------------------------------------------------------

    try:

        blockchain_tx_hash = store_bid_hash(
            str(bid.id),
            bid_hash
        )

        print("Blockchain Transaction:", blockchain_tx_hash)

    except Exception as e:

        print("❌ Blockchain transaction failed")
        print("Error:", str(e))

        blockchain_tx_hash = None


    # --------------------------------------------------------
    # 12. Save blockchain transaction hash in SQLite
    # --------------------------------------------------------

    bid.blockchain_tx_hash = blockchain_tx_hash

    db.commit()
    db.refresh(bid)


    # --------------------------------------------------------
    # 13. Return response
    # --------------------------------------------------------

    return {
        "message": "Bid placed successfully",

        "bid_id": bid.id,

        "amount": bid.amount,

        "bidder_id": bid.bidder_id,

        "tender_id": bid.tender_id,

        "created_at": bid.created_at,

        "bid_hash": bid.bid_hash,

        "blockchain_tx_hash": bid.blockchain_tx_hash
    }


# ============================================================
# GET ALL BIDS
# ============================================================

@router.get("/")
def get_bids(
    db: Session = Depends(get_db)
):

    return db.query(Bid).all()


# ============================================================
# GET SINGLE BID
# ============================================================

@router.get("/{bid_id}")
def get_bid(
    bid_id: int,
    db: Session = Depends(get_db)
):

    bid = db.query(Bid).filter(
        Bid.id == bid_id
    ).first()

    if not bid:
        raise HTTPException(
            status_code=404,
            detail="Bid not found"
        )

    return bid


# ============================================================
# VERIFY BID
# ============================================================

@router.get("/{bid_id}/verify")
def verify_bid(
    bid_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # 1. Find bid in database
    # --------------------------------------------------------

    bid = db.query(Bid).filter(
        Bid.id == bid_id
    ).first()

    if not bid:
        raise HTTPException(
            status_code=404,
            detail="Bid not found"
        )


    # --------------------------------------------------------
    # 2. Recreate original bid data
    # --------------------------------------------------------

    bid_data = {
        "amount": bid.amount,
        "bidder_id": bid.bidder_id,
        "tender_id": bid.tender_id,
        "created_at": bid.created_at.isoformat()
    }


    # --------------------------------------------------------
    # 3. Convert to same format
    # --------------------------------------------------------

    bid_string = json.dumps(
        bid_data,
        sort_keys=True
    )


    # --------------------------------------------------------
    # 4. Generate SHA-256 again
    # --------------------------------------------------------

    recalculated_hash = hashlib.sha256(
        bid_string.encode("utf-8")
    ).hexdigest()


    # --------------------------------------------------------
    # 5. Get hash from blockchain
    # --------------------------------------------------------

    try:

        blockchain_hash = get_bid_hash(
            str(bid.id)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not read hash from blockchain: {str(e)}"
        )


    # --------------------------------------------------------
    # 6. Compare database hash with recalculated hash
    # --------------------------------------------------------

    database_hash_valid = (
        recalculated_hash == bid.bid_hash
    )


    # --------------------------------------------------------
    # 7. Compare database hash with blockchain hash
    # --------------------------------------------------------

    blockchain_hash_valid = (
        blockchain_hash == bid.bid_hash
    )


    # --------------------------------------------------------
    # 8. Final verification
    # --------------------------------------------------------

    if database_hash_valid and blockchain_hash_valid:

        return {
            "bid_id": bid.id,

            "status": "VERIFIED",

            "message": "Bid is authentic and has not been tampered with.",

            "database_hash": bid.bid_hash,

            "recalculated_hash": recalculated_hash,

            "blockchain_hash": blockchain_hash,

            "database_hash_valid": True,

            "blockchain_hash_valid": True,

            "blockchain_tx_hash": bid.blockchain_tx_hash
        }


    else:

        return {
            "bid_id": bid.id,

            "status": "TAMPERING DETECTED",

            "message": "Bid data or blockchain record does not match.",

            "database_hash": bid.bid_hash,

            "recalculated_hash": recalculated_hash,

            "blockchain_hash": blockchain_hash,

            "database_hash_valid": database_hash_valid,

            "blockchain_hash_valid": blockchain_hash_valid,

            "blockchain_tx_hash": bid.blockchain_tx_hash
        }