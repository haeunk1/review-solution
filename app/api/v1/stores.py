from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.api import deps
from app.models.store import Store
from app.schemas.store import StoreCreate, StoreResponse

router = APIRouter()


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    business_type: Optional[str] = None
    naver_place_id: Optional[str] = None
    google_place_id: Optional[str] = None
    crawl_interval_hours: Optional[int] = None
    is_active: Optional[bool] = None


@router.post("/", response_model=StoreResponse)
def create_store(store_in: StoreCreate, db: Session = Depends(deps.get_db)):
    db_store = db.query(Store).filter(Store.store_id == store_in.store_id).first()
    if db_store:
        raise HTTPException(status_code=400, detail="이미 등록된 업장 ID입니다.")
    new_store = Store(**store_in.model_dump())
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    return new_store


@router.get("/", response_model=list[StoreResponse])
def get_stores(db: Session = Depends(deps.get_db)):
    return db.query(Store).all()


@router.get("/info/{store_id}", response_model=StoreResponse)
def get_store(store_id: str, db: Session = Depends(deps.get_db)):
    store = db.query(Store).filter(Store.store_id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="등록되지 않은 업장입니다.")
    return store


@router.patch("/{store_id}", response_model=StoreResponse)
def update_store(store_id: str, store_in: StoreUpdate, db: Session = Depends(deps.get_db)):
    store = db.query(Store).filter(Store.store_id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="업장을 찾을 수 없습니다.")
    for field, value in store_in.model_dump(exclude_none=True).items():
        setattr(store, field, value)
    db.commit()
    db.refresh(store)
    return store
