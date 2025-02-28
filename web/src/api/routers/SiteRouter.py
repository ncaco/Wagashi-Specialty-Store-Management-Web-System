from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SiteInfoVo import SiteInfo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/sites",
    tags=["sites"]
)

class SiteBase(BaseModel):
    ACNT_SN: int
    SITE_GRD_CD: str
    SITE_ID: str
    SITE_NM: str
    RPRS_ICON_PATH_NM: Optional[str] = None
    SITE_LOGO_NM: Optional[str] = None
    RMRK_CN: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

class SiteCreate(SiteBase):
    pass

class SiteResponse(SiteBase):
    SITE_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SiteResponse)
def create_site(site: SiteCreate, db: Session = Depends(get_db)):
    db_site = SiteInfo(
        **site.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@router.get("/", response_model=List[SiteResponse])
def read_sites(
    account_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SiteInfo)
    if account_sn:
        query = query.filter(SiteInfo.ACNT_SN == account_sn)
    sites = query.offset(skip).limit(limit).all()
    return sites

@router.get("/{site_sn}", response_model=SiteResponse)
def read_site(site_sn: int, db: Session = Depends(get_db)):
    site = db.query(SiteInfo).filter(SiteInfo.SITE_SN == site_sn).first()
    if site is None:
        raise HTTPException(status_code=404, detail="사이트를 찾을 수 없습니다")
    return site

@router.put("/{site_sn}", response_model=SiteResponse)
def update_site(site_sn: int, site: SiteBase, db: Session = Depends(get_db)):
    db_site = db.query(SiteInfo).filter(SiteInfo.SITE_SN == site_sn).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail="사이트를 찾을 수 없습니다")
    
    for key, value in site.dict(exclude_unset=True).items():
        setattr(db_site, key, value)
    
    db_site.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_site)
    return db_site

@router.delete("/{site_sn}")
def delete_site(site_sn: int, db: Session = Depends(get_db)):
    db_site = db.query(SiteInfo).filter(SiteInfo.SITE_SN == site_sn).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail="사이트를 찾을 수 없습니다")
    
    db.delete(db_site)
    db.commit()
    return {"message": "사이트가 삭제되었습니다"} 