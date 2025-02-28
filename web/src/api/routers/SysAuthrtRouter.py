from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SysAuthrtInfoVo import SystemAuthority
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/system-authorities",
    tags=["system-authorities"]
)

class SystemAuthorityBase(BaseModel):
    SITE_SN: int
    AUTHRT_NM: str
    AUTHRT_GRD_CD: str
    EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    AUTHRT_BGNG_DT: Optional[datetime] = None
    AUTHRT_END_DT: Optional[datetime] = None
    USE_YN: str = 'Y'
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None
    DEL_YN: str = 'N'
    DEL_YN_CHNRG_ID: Optional[str] = None
    DEL_YN_CHNRG_NM: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

class SystemAuthorityCreate(SystemAuthorityBase):
    pass

class SystemAuthorityResponse(SystemAuthorityBase):
    AUTHRT_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    DEL_YN_CHG_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SystemAuthorityResponse)
def create_authority(authority: SystemAuthorityCreate, db: Session = Depends(get_db)):
    db_authority = SystemAuthority(
        **authority.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_authority)
    db.commit()
    db.refresh(db_authority)
    return db_authority

@router.get("/", response_model=List[SystemAuthorityResponse])
def read_authorities(
    site_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SystemAuthority)
    if site_sn:
        query = query.filter(SystemAuthority.SITE_SN == site_sn)
    authorities = query.offset(skip).limit(limit).all()
    return authorities

@router.get("/{authority_sn}", response_model=SystemAuthorityResponse)
def read_authority(authority_sn: int, db: Session = Depends(get_db)):
    authority = db.query(SystemAuthority).filter(SystemAuthority.AUTHRT_SN == authority_sn).first()
    if authority is None:
        raise HTTPException(status_code=404, detail="권한을 찾을 수 없습니다")
    return authority

@router.put("/{authority_sn}", response_model=SystemAuthorityResponse)
def update_authority(authority_sn: int, authority: SystemAuthorityBase, db: Session = Depends(get_db)):
    db_authority = db.query(SystemAuthority).filter(SystemAuthority.AUTHRT_SN == authority_sn).first()
    if db_authority is None:
        raise HTTPException(status_code=404, detail="권한을 찾을 수 없습니다")
    
    for key, value in authority.dict(exclude_unset=True).items():
        setattr(db_authority, key, value)
    
    db_authority.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_authority)
    return db_authority

@router.delete("/{authority_sn}")
def delete_authority(authority_sn: int, db: Session = Depends(get_db)):
    db_authority = db.query(SystemAuthority).filter(SystemAuthority.AUTHRT_SN == authority_sn).first()
    if db_authority is None:
        raise HTTPException(status_code=404, detail="권한을 찾을 수 없습니다")
    
    db_authority.DEL_YN = 'Y'
    db_authority.DEL_YN_CHG_DT = datetime.now()
    db.commit()
    return {"message": "권한이 삭제되었습니다"} 