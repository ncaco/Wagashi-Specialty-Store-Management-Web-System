from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysAuthrtInfoModel import SysAuthrtInfo

router = APIRouter(
    prefix="/sysAuthrtInfo",
    tags=["SYS_AUTHRT_INFO"]
)

class SysAuthrtInfoBase(BaseModel):
    SITE_SN: int
    AUTHRT_NM: Optional[str] = None
    AUTHRT_GRD_CD: str
    EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    AUTHRT_BGNG_DT: Optional[datetime] = None
    AUTHRT_END_DT: Optional[datetime] = None
    USE_YN: Optional[str] = 'Y'
    DEL_YN: Optional[str] = None

class SysAuthrtInfoCreate(SysAuthrtInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysAuthrtInfoUpdate(SysAuthrtInfoBase):
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysAuthrtInfoResponse(SysAuthrtInfoBase):
    AUTHRT_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None
    DEL_YN_CHG_DT: Optional[datetime] = None
    DEL_YN_CHNRG_ID: Optional[str] = None
    DEL_YN_CHNRG_NM: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=SysAuthrtInfoResponse)
def create_authrt_info(authrt_info: SysAuthrtInfoCreate, db: Session = Depends(get_db)):
    db_authrt = SysAuthrtInfo(**authrt_info.dict())
    db_authrt.FRST_INPT_DT = datetime.now()
    
    db.add(db_authrt)
    db.commit()
    db.refresh(db_authrt)
    return db_authrt

@router.get("/", response_model=List[SysAuthrtInfoResponse])
def read_authrt_infos(
    skip: int = 0,
    limit: int = 100,
    site_sn: Optional[int] = None,
    authrt_grd_cd: Optional[str] = None,
    use_yn: Optional[str] = 'Y',
    del_yn: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SysAuthrtInfo)
    if site_sn:
        query = query.filter(SysAuthrtInfo.SITE_SN == site_sn)
    if authrt_grd_cd:
        query = query.filter(SysAuthrtInfo.AUTHRT_GRD_CD == authrt_grd_cd)
    if use_yn:
        query = query.filter(SysAuthrtInfo.USE_YN == use_yn)
    if del_yn:
        query = query.filter(SysAuthrtInfo.DEL_YN == del_yn)
    return query.offset(skip).limit(limit).all()

@router.get("/{authrt_sn}", response_model=SysAuthrtInfoResponse)
def read_authrt_info(authrt_sn: int, db: Session = Depends(get_db)):
    db_authrt = db.query(SysAuthrtInfo).filter(SysAuthrtInfo.AUTHRT_SN == authrt_sn).first()
    if db_authrt is None:
        raise HTTPException(status_code=404, detail="Authority not found")
    return db_authrt

@router.put("/{authrt_sn}", response_model=SysAuthrtInfoResponse)
def update_authrt_info(
    authrt_sn: int,
    authrt_info: SysAuthrtInfoUpdate,
    db: Session = Depends(get_db)
):
    db_authrt = db.query(SysAuthrtInfo).filter(SysAuthrtInfo.AUTHRT_SN == authrt_sn).first()
    if db_authrt is None:
        raise HTTPException(status_code=404, detail="Authority not found")
    
    update_data = authrt_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    if "USE_YN" in update_data and update_data["USE_YN"] != db_authrt.USE_YN:
        db_authrt.USE_YN_CHG_DT = datetime.now()
        db_authrt.USE_YN_CHNRG_ID = update_data["LAST_MDFR_ID"]
        db_authrt.USE_YN_CHNRG_NM = update_data["LAST_MDFR_NM"]
    
    if "DEL_YN" in update_data and update_data["DEL_YN"] != db_authrt.DEL_YN:
        db_authrt.DEL_YN_CHG_DT = datetime.now()
        db_authrt.DEL_YN_CHNRG_ID = update_data["LAST_MDFR_ID"]
        db_authrt.DEL_YN_CHNRG_NM = update_data["LAST_MDFR_NM"]
    
    for key, value in update_data.items():
        setattr(db_authrt, key, value)
    
    db.commit()
    db.refresh(db_authrt)
    return db_authrt

@router.delete("/{authrt_sn}")
def delete_authrt_info(
    authrt_sn: int,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_authrt = db.query(SysAuthrtInfo).filter(SysAuthrtInfo.AUTHRT_SN == authrt_sn).first()
    if db_authrt is None:
        raise HTTPException(status_code=404, detail="Authority not found")
    
    # 권한 상세 정보가 있는지 확인
    has_details = len(db_authrt.details) > 0
    if has_details:
        raise HTTPException(status_code=400, detail="Cannot delete authority that has detail information")
    
    db_authrt.DEL_YN = 'Y'
    db_authrt.DEL_YN_CHG_DT = datetime.now()
    db_authrt.DEL_YN_CHNRG_ID = del_id
    db_authrt.DEL_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"} 