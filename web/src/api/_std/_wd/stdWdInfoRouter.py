from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from database import get_db
from .stdWdInfoModel import StdWdInfo

router = APIRouter(
    prefix="/stdWdInfo",
    tags=["STD_WD_INFO"]
)

class StdWdInfoBase(BaseModel):
    STD_TYPE_CD: str = '0001'
    KORN_NM: str
    ENG_ABBR_NM: str
    ENG_NM: str
    WD_EXPLN: Optional[str] = None
    FORM_WD_YN: str = 'N'
    DOM_CLSF_NM: Optional[str] = None
    SYM_LST: Optional[str] = None
    PROH_WD_LST: Optional[str] = None
    WD_VER_NO: Optional[Decimal] = None
    STTS_NM: Optional[str] = None

class StdWdInfoCreate(StdWdInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class StdWdInfoUpdate(BaseModel):
    ENG_ABBR_NM: Optional[str] = None
    ENG_NM: Optional[str] = None
    WD_EXPLN: Optional[str] = None
    FORM_WD_YN: Optional[str] = None
    DOM_CLSF_NM: Optional[str] = None
    SYM_LST: Optional[str] = None
    PROH_WD_LST: Optional[str] = None
    WD_VER_NO: Optional[Decimal] = None
    STTS_NM: Optional[str] = None
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class StdWdInfoResponse(StdWdInfoBase):
    WD_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    LAST_MDFCN_DT: Optional[datetime] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=StdWdInfoResponse)
def create_word(word: StdWdInfoCreate, db: Session = Depends(get_db)):
    db_word = StdWdInfo(**word.model_dump())
    try:
        db.add(db_word)
        db.commit()
        db.refresh(db_word)
        return db_word
    except Exception as e:
        db.rollback()
        if "KORN_NM" in str(e):
            raise HTTPException(status_code=400, detail="한글명이 이미 존재합니다")
        if "ENG_ABBR_NM" in str(e):
            raise HTTPException(status_code=400, detail="영문약어명이 이미 존재합니다")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[StdWdInfoResponse])
def read_words(
    skip: int = 0,
    limit: int = 100,
    korn_nm: Optional[str] = None,
    eng_abbr_nm: Optional[str] = None,
    std_type_cd: Optional[str] = None,
    form_wd_yn: Optional[str] = None,
    dom_clsf_nm: Optional[str] = None,
    stts_nm: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(StdWdInfo)
    if korn_nm:
        query = query.filter(StdWdInfo.KORN_NM.like(f"%{korn_nm}%"))
    if eng_abbr_nm:
        query = query.filter(StdWdInfo.ENG_ABBR_NM.like(f"%{eng_abbr_nm}%"))
    if std_type_cd:
        query = query.filter(StdWdInfo.STD_TYPE_CD == std_type_cd)
    if form_wd_yn:
        query = query.filter(StdWdInfo.FORM_WD_YN == form_wd_yn)
    if dom_clsf_nm:
        query = query.filter(StdWdInfo.DOM_CLSF_NM.like(f"%{dom_clsf_nm}%"))
    if stts_nm:
        query = query.filter(StdWdInfo.STTS_NM == stts_nm)
    return query.offset(skip).limit(limit).all()

@router.get("/{wd_sn}", response_model=StdWdInfoResponse)
def read_word(wd_sn: int, db: Session = Depends(get_db)):
    db_word = db.query(StdWdInfo).filter(StdWdInfo.WD_SN == wd_sn).first()
    if db_word is None:
        raise HTTPException(status_code=404, detail="단어를 찾을 수 없습니다")
    return db_word

@router.put("/{wd_sn}", response_model=StdWdInfoResponse)
def update_word(wd_sn: int, word: StdWdInfoUpdate, db: Session = Depends(get_db)):
    db_word = db.query(StdWdInfo).filter(StdWdInfo.WD_SN == wd_sn).first()
    if db_word is None:
        raise HTTPException(status_code=404, detail="단어를 찾을 수 없습니다")
    
    update_data = word.model_dump(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    try:
        for key, value in update_data.items():
            setattr(db_word, key, value)
        db.commit()
        db.refresh(db_word)
        return db_word
    except Exception as e:
        db.rollback()
        if "ENG_ABBR_NM" in str(e):
            raise HTTPException(status_code=400, detail="영문약어명이 이미 존재합니다")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check/duplicate", response_model=dict)
def check_duplicate(
    korn_nm: Optional[str] = None,
    eng_abbr_nm: Optional[str] = None,
    db: Session = Depends(get_db)
):
    result = {"korn_nm": False, "eng_abbr_nm": False}
    
    if korn_nm:
        exists = db.query(StdWdInfo).filter(StdWdInfo.KORN_NM == korn_nm).first()
        result["korn_nm"] = exists is not None
        
    if eng_abbr_nm:
        exists = db.query(StdWdInfo).filter(StdWdInfo.ENG_ABBR_NM == eng_abbr_nm).first()
        result["eng_abbr_nm"] = exists is not None
        
    return result 