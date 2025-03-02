from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .stdVocabInfoModel import StdVocabInfo

router = APIRouter(
    prefix="/stdVocabInfo",
    tags=["STD_VOCAB_INFO"]
)

class StdVocabInfoBase(BaseModel):
    STD_TYPE_CD: str
    KORN_VOCAB_NM: str
    ENG_ABBR_NM: str
    STD_DOM_CLSF_NM: str
    STD_DOM_CD_NM: str
    VOCAB_EXPLN: Optional[str] = None
    PBADMS_STD_CD_NM: Optional[str] = None
    AFFL_INST_NM: Optional[str] = None
    VOCAB_SYM_LST: Optional[str] = None

class StdVocabInfoCreate(StdVocabInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class StdVocabInfoUpdate(BaseModel):
    VOCAB_EXPLN: Optional[str] = None
    PBADMS_STD_CD_NM: Optional[str] = None
    AFFL_INST_NM: Optional[str] = None
    VOCAB_SYM_LST: Optional[str] = None
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class StdVocabInfoResponse(StdVocabInfoBase):
    VOCAB_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    LAST_MDFCN_DT: Optional[datetime] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=StdVocabInfoResponse)
def create_vocab(vocab: StdVocabInfoCreate, db: Session = Depends(get_db)):
    db_vocab = StdVocabInfo(**vocab.model_dump())
    try:
        db.add(db_vocab)
        db.commit()
        db.refresh(db_vocab)
        return db_vocab
    except Exception as e:
        db.rollback()
        if "KORN_VOCAB_NM" in str(e):
            raise HTTPException(status_code=400, detail="한글용어명이 이미 존재합니다")
        if "ENG_ABBR_NM" in str(e):
            raise HTTPException(status_code=400, detail="영문약어명이 이미 존재합니다")
        if "STD_DOM_INFO" in str(e):
            raise HTTPException(status_code=400, detail="유효하지 않은 도메인 정보입니다")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[StdVocabInfoResponse])
def read_vocabs(
    skip: int = 0,
    limit: int = 100,
    korn_vocab_nm: Optional[str] = None,
    eng_abbr_nm: Optional[str] = None,
    std_type_cd: Optional[str] = None,
    std_dom_clsf_nm: Optional[str] = None,
    std_dom_cd_nm: Optional[str] = None,
    affl_inst_nm: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(StdVocabInfo)
    if korn_vocab_nm:
        query = query.filter(StdVocabInfo.KORN_VOCAB_NM.like(f"%{korn_vocab_nm}%"))
    if eng_abbr_nm:
        query = query.filter(StdVocabInfo.ENG_ABBR_NM.like(f"%{eng_abbr_nm}%"))
    if std_type_cd:
        query = query.filter(StdVocabInfo.STD_TYPE_CD == std_type_cd)
    if std_dom_clsf_nm:
        query = query.filter(StdVocabInfo.STD_DOM_CLSF_NM == std_dom_clsf_nm)
    if std_dom_cd_nm:
        query = query.filter(StdVocabInfo.STD_DOM_CD_NM == std_dom_cd_nm)
    if affl_inst_nm:
        query = query.filter(StdVocabInfo.AFFL_INST_NM.like(f"%{affl_inst_nm}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/{vocab_sn}", response_model=StdVocabInfoResponse)
def read_vocab(vocab_sn: int, db: Session = Depends(get_db)):
    db_vocab = db.query(StdVocabInfo).filter(StdVocabInfo.VOCAB_SN == vocab_sn).first()
    if db_vocab is None:
        raise HTTPException(status_code=404, detail="용어를 찾을 수 없습니다")
    return db_vocab

@router.put("/{vocab_sn}", response_model=StdVocabInfoResponse)
def update_vocab(vocab_sn: int, vocab: StdVocabInfoUpdate, db: Session = Depends(get_db)):
    db_vocab = db.query(StdVocabInfo).filter(StdVocabInfo.VOCAB_SN == vocab_sn).first()
    if db_vocab is None:
        raise HTTPException(status_code=404, detail="용어를 찾을 수 없습니다")
    
    update_data = vocab.model_dump(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    try:
        for key, value in update_data.items():
            setattr(db_vocab, key, value)
        db.commit()
        db.refresh(db_vocab)
        return db_vocab
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check/duplicate", response_model=dict)
def check_duplicate(
    korn_vocab_nm: Optional[str] = None,
    eng_abbr_nm: Optional[str] = None,
    db: Session = Depends(get_db)
):
    result = {"korn_vocab_nm": False, "eng_abbr_nm": False}
    
    if korn_vocab_nm:
        exists = db.query(StdVocabInfo).filter(StdVocabInfo.KORN_VOCAB_NM == korn_vocab_nm).first()
        result["korn_vocab_nm"] = exists is not None
        
    if eng_abbr_nm:
        exists = db.query(StdVocabInfo).filter(StdVocabInfo.ENG_ABBR_NM == eng_abbr_nm).first()
        result["eng_abbr_nm"] = exists is not None
        
    return result 