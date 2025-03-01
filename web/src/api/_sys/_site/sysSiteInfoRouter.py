from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysSiteInfoModel import SysSiteInfo

router = APIRouter(
    prefix="/sysSiteInfo",
    tags=["SYS_SITE_INFO"]
)

class SysSiteInfoBase(BaseModel):
    SITE_ID: Optional[str] = None
    SITE_NM: str
    SITE_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    USE_YN: Optional[str] = 'Y'
    ATCH_FILE_SN: Optional[int] = None
    ICON_SN: Optional[int] = None

class SysSiteInfoCreate(SysSiteInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysSiteInfoUpdate(SysSiteInfoBase):
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysSiteInfoResponse(SysSiteInfoBase):
    SITE_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=SysSiteInfoResponse)
def create_site_info(site_info: SysSiteInfoCreate, db: Session = Depends(get_db)):
    db_site = SysSiteInfo(**site_info.dict())
    db_site.FRST_INPT_DT = datetime.now()
    
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@router.get("/", response_model=List[SysSiteInfoResponse])
def read_site_infos(
    skip: int = 0,
    limit: int = 100,
    site_id: Optional[str] = None,
    use_yn: Optional[str] = 'Y',
    db: Session = Depends(get_db)
):
    query = db.query(SysSiteInfo)
    if site_id:
        query = query.filter(SysSiteInfo.SITE_ID == site_id)
    if use_yn:
        query = query.filter(SysSiteInfo.USE_YN == use_yn)
    return query.offset(skip).limit(limit).all()

@router.get("/{site_sn}", response_model=SysSiteInfoResponse)
def read_site_info(site_sn: int, db: Session = Depends(get_db)):
    db_site = db.query(SysSiteInfo).filter(SysSiteInfo.SITE_SN == site_sn).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site

@router.put("/{site_sn}", response_model=SysSiteInfoResponse)
def update_site_info(
    site_sn: int,
    site_info: SysSiteInfoUpdate,
    db: Session = Depends(get_db)
):
    db_site = db.query(SysSiteInfo).filter(SysSiteInfo.SITE_SN == site_sn).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    
    update_data = site_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    for key, value in update_data.items():
        setattr(db_site, key, value)
    
    db.commit()
    db.refresh(db_site)
    return db_site

@router.delete("/{site_sn}")
def delete_site_info(
    site_sn: int,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_site = db.query(SysSiteInfo).filter(SysSiteInfo.SITE_SN == site_sn).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_site.DEL_YN = 'Y'
    db_site.DEL_YN_CHG_DT = datetime.now()
    db_site.DEL_YN_CHNRG_ID = del_id
    db_site.DEL_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"}
