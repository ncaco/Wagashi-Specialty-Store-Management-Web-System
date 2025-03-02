from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysPrgrmInfoModel import SysPrgrmInfo

router = APIRouter(
    prefix="/sysPrgrmInfo",
    tags=["SYS_PRGRM_INFO"]
)

class SysPrgrmInfoBase(BaseModel):
    PRGRM_ID: Optional[str] = None
    PRGRM_NM: str
    PRGRM_PATH_NM: Optional[str] = None
    PRGRM_SE_CD: Optional[str] = None
    PRGRM_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    SORT_SN: Optional[int] = None
    ATCH_FILE_SN: Optional[int] = None

class SysPrgrmInfoCreate(SysPrgrmInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysPrgrmInfoUpdate(SysPrgrmInfoBase):
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysPrgrmInfoResponse(SysPrgrmInfoBase):
    PRGRM_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=SysPrgrmInfoResponse)
def create_prgrm_info(prgrm_info: SysPrgrmInfoCreate, db: Session = Depends(get_db)):
    db_prgrm = SysPrgrmInfo(**prgrm_info.dict())
    db_prgrm.FRST_INPT_DT = datetime.now()
    
    db.add(db_prgrm)
    db.commit()
    db.refresh(db_prgrm)
    return db_prgrm

@router.get("/", response_model=List[SysPrgrmInfoResponse])
def read_prgrm_infos(
    skip: int = 0,
    limit: int = 100,
    prgrm_id: Optional[str] = None,
    prgrm_se_cd: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SysPrgrmInfo)
    if prgrm_id:
        query = query.filter(SysPrgrmInfo.PRGRM_ID == prgrm_id)
    if prgrm_se_cd:
        query = query.filter(SysPrgrmInfo.PRGRM_SE_CD == prgrm_se_cd)
    return query.offset(skip).limit(limit).all()

@router.get("/{prgrm_sn}", response_model=SysPrgrmInfoResponse)
def read_prgrm_info(prgrm_sn: int, db: Session = Depends(get_db)):
    db_prgrm = db.query(SysPrgrmInfo).filter(SysPrgrmInfo.PRGRM_SN == prgrm_sn).first()
    if db_prgrm is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return db_prgrm

@router.put("/{prgrm_sn}", response_model=SysPrgrmInfoResponse)
def update_prgrm_info(
    prgrm_sn: int,
    prgrm_info: SysPrgrmInfoUpdate,
    db: Session = Depends(get_db)
):
    db_prgrm = db.query(SysPrgrmInfo).filter(SysPrgrmInfo.PRGRM_SN == prgrm_sn).first()
    if db_prgrm is None:
        raise HTTPException(status_code=404, detail="Program not found")
    
    update_data = prgrm_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    for key, value in update_data.items():
        setattr(db_prgrm, key, value)
    
    db.commit()
    db.refresh(db_prgrm)
    return db_prgrm

@router.delete("/{prgrm_sn}")
def delete_prgrm_info(
    prgrm_sn: int,
    db: Session = Depends(get_db)
):
    db_prgrm = db.query(SysPrgrmInfo).filter(SysPrgrmInfo.PRGRM_SN == prgrm_sn).first()
    if db_prgrm is None:
        raise HTTPException(status_code=404, detail="Program not found")
    
    db.delete(db_prgrm)
    db.commit()
    return {"message": "Successfully deleted"} 