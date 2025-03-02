from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .stdDomInfoModel import StdDomInfo

router = APIRouter(
    prefix="/stdDomInfo",
    tags=["STD_DOM_INFO"]
)

class StdDomInfoBase(BaseModel):
    STD_TYPE_CD: str = '0001'
    STD_DOM_GROUP_NM: str
    STD_DOM_CLSF_NM: str
    STD_DOM_CD_NM: str
    STD_DOM_NM: str
    STD_DOM_EXPLN: Optional[str] = None
    DATA_TYPE_NM: Optional[str] = None
    DATA_SZ: Optional[int] = None
    DATA_DP_SZ: Optional[int] = None
    STRG_FORM_NM: Optional[str] = None
    EXPR_FORM_NM: Optional[str] = None
    UNIT_NM: Optional[str] = None
    ALLOW_VL_CN: Optional[str] = None

class StdDomInfoCreate(StdDomInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class StdDomInfoUpdate(BaseModel):
    STD_DOM_GROUP_NM: Optional[str] = None
    STD_DOM_NM: Optional[str] = None
    STD_DOM_EXPLN: Optional[str] = None
    DATA_TYPE_NM: Optional[str] = None
    DATA_SZ: Optional[int] = None
    DATA_DP_SZ: Optional[int] = None
    STRG_FORM_NM: Optional[str] = None
    EXPR_FORM_NM: Optional[str] = None
    UNIT_NM: Optional[str] = None
    ALLOW_VL_CN: Optional[str] = None
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class StdDomInfoResponse(StdDomInfoBase):
    DOM_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    LAST_MDFCN_DT: Optional[datetime] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=StdDomInfoResponse)
def create_domain(domain: StdDomInfoCreate, db: Session = Depends(get_db)):
    db_domain = StdDomInfo(**domain.model_dump())
    try:
        db.add(db_domain)
        db.commit()
        db.refresh(db_domain)
        return db_domain
    except Exception as e:
        db.rollback()
        if "UN1" in str(e):
            raise HTTPException(
                status_code=400, 
                detail="동일한 도메인분류명과 도메인코드명이 이미 존재합니다"
            )
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[StdDomInfoResponse])
def read_domains(
    skip: int = 0,
    limit: int = 100,
    std_dom_group_nm: Optional[str] = None,
    std_dom_clsf_nm: Optional[str] = None,
    std_dom_cd_nm: Optional[str] = None,
    std_dom_nm: Optional[str] = None,
    data_type_nm: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(StdDomInfo)
    if std_dom_group_nm:
        query = query.filter(StdDomInfo.STD_DOM_GROUP_NM.like(f"%{std_dom_group_nm}%"))
    if std_dom_clsf_nm:
        query = query.filter(StdDomInfo.STD_DOM_CLSF_NM.like(f"%{std_dom_clsf_nm}%"))
    if std_dom_cd_nm:
        query = query.filter(StdDomInfo.STD_DOM_CD_NM.like(f"%{std_dom_cd_nm}%"))
    if std_dom_nm:
        query = query.filter(StdDomInfo.STD_DOM_NM.like(f"%{std_dom_nm}%"))
    if data_type_nm:
        query = query.filter(StdDomInfo.DATA_TYPE_NM == data_type_nm)
    return query.offset(skip).limit(limit).all()

@router.get("/{dom_sn}", response_model=StdDomInfoResponse)
def read_domain(dom_sn: int, db: Session = Depends(get_db)):
    db_domain = db.query(StdDomInfo).filter(StdDomInfo.DOM_SN == dom_sn).first()
    if db_domain is None:
        raise HTTPException(status_code=404, detail="도메인을 찾을 수 없습니다")
    return db_domain

@router.put("/{dom_sn}", response_model=StdDomInfoResponse)
def update_domain(dom_sn: int, domain: StdDomInfoUpdate, db: Session = Depends(get_db)):
    db_domain = db.query(StdDomInfo).filter(StdDomInfo.DOM_SN == dom_sn).first()
    if db_domain is None:
        raise HTTPException(status_code=404, detail="도메인을 찾을 수 없습니다")
    
    update_data = domain.model_dump(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    try:
        for key, value in update_data.items():
            setattr(db_domain, key, value)
        db.commit()
        db.refresh(db_domain)
        return db_domain
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check/duplicate", response_model=dict)
def check_duplicate(
    std_dom_clsf_nm: Optional[str] = None,
    std_dom_cd_nm: Optional[str] = None,
    db: Session = Depends(get_db)
):
    result = {"exists": False}
    
    if std_dom_clsf_nm and std_dom_cd_nm:
        exists = db.query(StdDomInfo).filter(
            StdDomInfo.STD_DOM_CLSF_NM == std_dom_clsf_nm,
            StdDomInfo.STD_DOM_CD_NM == std_dom_cd_nm
        ).first()
        result["exists"] = exists is not None
        
    return result 