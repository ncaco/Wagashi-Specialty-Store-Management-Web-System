from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysAuthrtDtlInfoModel import SysAuthrtDtlInfo

router = APIRouter(
    prefix="/sysAuthrtDtlInfo",
    tags=["SYS_AUTHRT_DTL_INFO"]
)

class SysAuthrtDtlInfoBase(BaseModel):
    AUTHRT_SN: int
    MENU_SN: int
    PRCS_SE_CD: str
    ACTVTN_YN: str = 'Y'

class SysAuthrtDtlInfoCreate(SysAuthrtDtlInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysAuthrtDtlInfoUpdate(BaseModel):
    ACTVTN_YN: str
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysAuthrtDtlInfoResponse(SysAuthrtDtlInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=SysAuthrtDtlInfoResponse)
def create_authrt_dtl_info(authrt_dtl_info: SysAuthrtDtlInfoCreate, db: Session = Depends(get_db)):
    # 중복 체크
    existing_dtl = db.query(SysAuthrtDtlInfo).filter(
        SysAuthrtDtlInfo.AUTHRT_SN == authrt_dtl_info.AUTHRT_SN,
        SysAuthrtDtlInfo.MENU_SN == authrt_dtl_info.MENU_SN,
        SysAuthrtDtlInfo.PRCS_SE_CD == authrt_dtl_info.PRCS_SE_CD
    ).first()
    if existing_dtl:
        raise HTTPException(status_code=400, detail="Authority detail already exists")
    
    db_authrt_dtl = SysAuthrtDtlInfo(**authrt_dtl_info.dict())
    db_authrt_dtl.FRST_INPT_DT = datetime.now()
    
    db.add(db_authrt_dtl)
    db.commit()
    db.refresh(db_authrt_dtl)
    return db_authrt_dtl

@router.get("/", response_model=List[SysAuthrtDtlInfoResponse])
def read_authrt_dtl_infos(
    skip: int = 0,
    limit: int = 100,
    authrt_sn: Optional[int] = None,
    menu_sn: Optional[int] = None,
    prcs_se_cd: Optional[str] = None,
    actvtn_yn: Optional[str] = 'Y',
    db: Session = Depends(get_db)
):
    query = db.query(SysAuthrtDtlInfo)
    if authrt_sn:
        query = query.filter(SysAuthrtDtlInfo.AUTHRT_SN == authrt_sn)
    if menu_sn:
        query = query.filter(SysAuthrtDtlInfo.MENU_SN == menu_sn)
    if prcs_se_cd:
        query = query.filter(SysAuthrtDtlInfo.PRCS_SE_CD == prcs_se_cd)
    if actvtn_yn:
        query = query.filter(SysAuthrtDtlInfo.ACTVTN_YN == actvtn_yn)
    return query.offset(skip).limit(limit).all()

@router.get("/{authrt_sn}/{menu_sn}/{prcs_se_cd}", response_model=SysAuthrtDtlInfoResponse)
def read_authrt_dtl_info(
    authrt_sn: int,
    menu_sn: int,
    prcs_se_cd: str,
    db: Session = Depends(get_db)
):
    db_authrt_dtl = db.query(SysAuthrtDtlInfo).filter(
        SysAuthrtDtlInfo.AUTHRT_SN == authrt_sn,
        SysAuthrtDtlInfo.MENU_SN == menu_sn,
        SysAuthrtDtlInfo.PRCS_SE_CD == prcs_se_cd
    ).first()
    if db_authrt_dtl is None:
        raise HTTPException(status_code=404, detail="Authority detail not found")
    return db_authrt_dtl

@router.put("/{authrt_sn}/{menu_sn}/{prcs_se_cd}", response_model=SysAuthrtDtlInfoResponse)
def update_authrt_dtl_info(
    authrt_sn: int,
    menu_sn: int,
    prcs_se_cd: str,
    authrt_dtl_info: SysAuthrtDtlInfoUpdate,
    db: Session = Depends(get_db)
):
    db_authrt_dtl = db.query(SysAuthrtDtlInfo).filter(
        SysAuthrtDtlInfo.AUTHRT_SN == authrt_sn,
        SysAuthrtDtlInfo.MENU_SN == menu_sn,
        SysAuthrtDtlInfo.PRCS_SE_CD == prcs_se_cd
    ).first()
    if db_authrt_dtl is None:
        raise HTTPException(status_code=404, detail="Authority detail not found")
    
    update_data = authrt_dtl_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    for key, value in update_data.items():
        setattr(db_authrt_dtl, key, value)
    
    db.commit()
    db.refresh(db_authrt_dtl)
    return db_authrt_dtl

@router.delete("/{authrt_sn}/{menu_sn}/{prcs_se_cd}")
def delete_authrt_dtl_info(
    authrt_sn: int,
    menu_sn: int,
    prcs_se_cd: str,
    db: Session = Depends(get_db)
):
    db_authrt_dtl = db.query(SysAuthrtDtlInfo).filter(
        SysAuthrtDtlInfo.AUTHRT_SN == authrt_sn,
        SysAuthrtDtlInfo.MENU_SN == menu_sn,
        SysAuthrtDtlInfo.PRCS_SE_CD == prcs_se_cd
    ).first()
    if db_authrt_dtl is None:
        raise HTTPException(status_code=404, detail="Authority detail not found")
    
    db.delete(db_authrt_dtl)
    db.commit()
    return {"message": "Successfully deleted"} 