from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SysCtgryInfoVo import SystemCategory
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/system-categories",
    tags=["system-categories"]
)

class SystemCategoryBase(BaseModel):
    UP_CTGRY_SN: Optional[int] = None
    CTGRY_NM: str
    CTGRY_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    USE_YN: str = 'Y'
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    SORT_SN: Optional[int] = None

class SystemCategoryCreate(SystemCategoryBase):
    pass

class SystemCategoryResponse(SystemCategoryBase):
    CTGRY_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SystemCategoryResponse)
def create_category(category: SystemCategoryCreate, db: Session = Depends(get_db)):
    db_category = SystemCategory(
        **category.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=List[SystemCategoryResponse])
def read_categories(
    up_category_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SystemCategory)
    if up_category_sn:
        query = query.filter(SystemCategory.UP_CTGRY_SN == up_category_sn)
    categories = query.offset(skip).limit(limit).all()
    return categories

@router.get("/{category_sn}", response_model=SystemCategoryResponse)
def read_category(category_sn: int, db: Session = Depends(get_db)):
    category = db.query(SystemCategory).filter(SystemCategory.CTGRY_SN == category_sn).first()
    if category is None:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
    return category

@router.put("/{category_sn}", response_model=SystemCategoryResponse)
def update_category(category_sn: int, category: SystemCategoryBase, db: Session = Depends(get_db)):
    db_category = db.query(SystemCategory).filter(SystemCategory.CTGRY_SN == category_sn).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
    
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    
    db_category.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_sn}")
def delete_category(category_sn: int, db: Session = Depends(get_db)):
    db_category = db.query(SystemCategory).filter(SystemCategory.CTGRY_SN == category_sn).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
    
    db_category.USE_YN = 'N'
    db_category.USE_YN_CHG_DT = datetime.now()
    db.commit()
    return {"message": "카테고리가 비활성화되었습니다"} 