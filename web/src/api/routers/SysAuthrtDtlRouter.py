from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SysAuthrtDtlInfoVo import SystemAuthorityDetail
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/system-authority-details",
    tags=["system-authority-details"]
)

class SystemAuthorityDetailBase(BaseModel):
    AUTHRT_SN: int
    MENU_SN: int
    PRCS_SE_CD: str
    ACTVTN_YN: str = 'Y'
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

class SystemAuthorityDetailCreate(SystemAuthorityDetailBase):
    pass

class SystemAuthorityDetailResponse(SystemAuthorityDetailBase):
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SystemAuthorityDetailResponse)
def create_authority_detail(authority_detail: SystemAuthorityDetailCreate, db: Session = Depends(get_db)):
    db_authority_detail = SystemAuthorityDetail(
        **authority_detail.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_authority_detail)
    db.commit()
    db.refresh(db_authority_detail)
    return db_authority_detail

@router.get("/", response_model=List[SystemAuthorityDetailResponse])
def read_authority_details(
    authority_sn: Optional[int] = None,
    menu_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SystemAuthorityDetail)
    if authority_sn:
        query = query.filter(SystemAuthorityDetail.AUTHRT_SN == authority_sn)
    if menu_sn:
        query = query.filter(SystemAuthorityDetail.MENU_SN == menu_sn)
    authority_details = query.offset(skip).limit(limit).all()
    return authority_details

@router.get("/{authority_sn}/{menu_sn}", response_model=SystemAuthorityDetailResponse)
def read_authority_detail(authority_sn: int, menu_sn: int, db: Session = Depends(get_db)):
    authority_detail = db.query(SystemAuthorityDetail).filter(
        SystemAuthorityDetail.AUTHRT_SN == authority_sn,
        SystemAuthorityDetail.MENU_SN == menu_sn
    ).first()
    if authority_detail is None:
        raise HTTPException(status_code=404, detail="권한 상세 정보를 찾을 수 없습니다")
    return authority_detail

@router.put("/{authority_sn}/{menu_sn}", response_model=SystemAuthorityDetailResponse)
def update_authority_detail(
    authority_sn: int,
    menu_sn: int,
    authority_detail: SystemAuthorityDetailBase,
    db: Session = Depends(get_db)
):
    db_authority_detail = db.query(SystemAuthorityDetail).filter(
        SystemAuthorityDetail.AUTHRT_SN == authority_sn,
        SystemAuthorityDetail.MENU_SN == menu_sn
    ).first()
    if db_authority_detail is None:
        raise HTTPException(status_code=404, detail="권한 상세 정보를 찾을 수 없습니다")
    
    for key, value in authority_detail.dict(exclude_unset=True).items():
        setattr(db_authority_detail, key, value)
    
    db_authority_detail.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_authority_detail)
    return db_authority_detail

@router.delete("/{authority_sn}/{menu_sn}")
def delete_authority_detail(authority_sn: int, menu_sn: int, db: Session = Depends(get_db)):
    db_authority_detail = db.query(SystemAuthorityDetail).filter(
        SystemAuthorityDetail.AUTHRT_SN == authority_sn,
        SystemAuthorityDetail.MENU_SN == menu_sn
    ).first()
    if db_authority_detail is None:
        raise HTTPException(status_code=404, detail="권한 상세 정보를 찾을 수 없습니다")
    
    db.delete(db_authority_detail)
    db.commit()
    return {"message": "권한 상세 정보가 삭제되었습니다"} 