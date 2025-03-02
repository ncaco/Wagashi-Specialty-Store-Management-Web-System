from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysCtgryInfoModel import SysCtgryInfo

router = APIRouter(
    prefix="/sysCtgryInfo",
    tags=["SYS_CTGRY_INFO"]
)

class SysCtgryInfoBase(BaseModel):
    UP_CTGRY_SN: Optional[int] = None
    CTGRY_NM: str
    CTGRY_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    USE_YN: Optional[str] = 'Y'
    SORT_SN: Optional[int] = None

class SysCtgryInfoCreate(SysCtgryInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysCtgryInfoUpdate(SysCtgryInfoBase):
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysCtgryInfoResponse(SysCtgryInfoBase):
    CTGRY_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=SysCtgryInfoResponse)
def create_ctgry_info(ctgry_info: SysCtgryInfoCreate, db: Session = Depends(get_db)):
    db_ctgry = SysCtgryInfo(**ctgry_info.dict())
    db_ctgry.FRST_INPT_DT = datetime.now()
    
    db.add(db_ctgry)
    db.commit()
    db.refresh(db_ctgry)
    return db_ctgry

@router.get("/", response_model=List[SysCtgryInfoResponse])
def read_ctgry_infos(
    skip: int = 0,
    limit: int = 100,
    up_ctgry_sn: Optional[int] = None,
    use_yn: Optional[str] = 'Y',
    db: Session = Depends(get_db)
):
    query = db.query(SysCtgryInfo)
    if up_ctgry_sn:
        query = query.filter(SysCtgryInfo.UP_CTGRY_SN == up_ctgry_sn)
    if use_yn:
        query = query.filter(SysCtgryInfo.USE_YN == use_yn)
    return query.order_by(SysCtgryInfo.SORT_SN).offset(skip).limit(limit).all()

@router.get("/{ctgry_sn}", response_model=SysCtgryInfoResponse)
def read_ctgry_info(ctgry_sn: int, db: Session = Depends(get_db)):
    db_ctgry = db.query(SysCtgryInfo).filter(SysCtgryInfo.CTGRY_SN == ctgry_sn).first()
    if db_ctgry is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_ctgry

@router.put("/{ctgry_sn}", response_model=SysCtgryInfoResponse)
def update_ctgry_info(
    ctgry_sn: int,
    ctgry_info: SysCtgryInfoUpdate,
    db: Session = Depends(get_db)
):
    db_ctgry = db.query(SysCtgryInfo).filter(SysCtgryInfo.CTGRY_SN == ctgry_sn).first()
    if db_ctgry is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = ctgry_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    if "USE_YN" in update_data and update_data["USE_YN"] != db_ctgry.USE_YN:
        db_ctgry.USE_YN_CHG_DT = datetime.now()
        db_ctgry.USE_YN_CHNRG_ID = update_data["LAST_MDFR_ID"]
        db_ctgry.USE_YN_CHNRG_NM = update_data["LAST_MDFR_NM"]
    
    for key, value in update_data.items():
        setattr(db_ctgry, key, value)
    
    db.commit()
    db.refresh(db_ctgry)
    return db_ctgry

@router.delete("/{ctgry_sn}")
def delete_ctgry_info(
    ctgry_sn: int,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_ctgry = db.query(SysCtgryInfo).filter(SysCtgryInfo.CTGRY_SN == ctgry_sn).first()
    if db_ctgry is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # 하위 범주가 있는지 확인
    has_children = db.query(SysCtgryInfo).filter(SysCtgryInfo.UP_CTGRY_SN == ctgry_sn).first() is not None
    if has_children:
        raise HTTPException(status_code=400, detail="Cannot delete category with subcategories")
    
    db_ctgry.USE_YN = 'N'
    db_ctgry.USE_YN_CHG_DT = datetime.now()
    db_ctgry.USE_YN_CHNRG_ID = del_id
    db_ctgry.USE_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"} 