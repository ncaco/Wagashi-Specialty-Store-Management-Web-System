from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysAnsInfoModel import SysAnsInfo

router = APIRouter(
    prefix="/sysAnsInfo",
    tags=["시스템 관련/답변 관련"]
)

class SysAnsInfoBase(BaseModel):
    PST_SN: int
    UP_ANS_SN: Optional[int] = None
    ANS_CN: str
    SECRT_YN: Optional[str] = 'N'
    EMTCN_SN: Optional[int] = None

class SysAnsInfoCreate(SysAnsInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysAnsInfoUpdate(BaseModel):
    ANS_CN: Optional[str] = None
    SECRT_YN: Optional[str] = None
    EMTCN_SN: Optional[int] = None
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysAnsInfoResponse(SysAnsInfoBase):
    ANS_SN: int
    DEL_YN: Optional[str] = None
    DEL_YN_CHG_DT: Optional[datetime] = None
    DEL_YN_CHNRG_ID: Optional[str] = None
    DEL_YN_CHNRG_NM: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=SysAnsInfoResponse)
def create_ans(ans: SysAnsInfoCreate, db: Session = Depends(get_db)):
    db_ans = SysAnsInfo(**ans.model_dump())
    db.add(db_ans)
    db.commit()
    db.refresh(db_ans)
    return db_ans

@router.get("/", response_model=List[SysAnsInfoResponse])
def read_answers(
    skip: int = 0,
    limit: int = 100,
    pst_sn: Optional[int] = None,
    up_ans_sn: Optional[int] = None,
    del_yn: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SysAnsInfo)
    if pst_sn:
        query = query.filter(SysAnsInfo.PST_SN == pst_sn)
    if up_ans_sn:
        query = query.filter(SysAnsInfo.UP_ANS_SN == up_ans_sn)
    if del_yn:
        query = query.filter(SysAnsInfo.DEL_YN == del_yn)
    return query.offset(skip).limit(limit).all()

@router.get("/{ans_sn}", response_model=SysAnsInfoResponse)
def read_ans(ans_sn: int, db: Session = Depends(get_db)):
    db_ans = db.query(SysAnsInfo).filter(SysAnsInfo.ANS_SN == ans_sn).first()
    if db_ans is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return db_ans

@router.put("/{ans_sn}", response_model=SysAnsInfoResponse)
def update_ans(ans_sn: int, ans: SysAnsInfoUpdate, db: Session = Depends(get_db)):
    db_ans = db.query(SysAnsInfo).filter(SysAnsInfo.ANS_SN == ans_sn).first()
    if db_ans is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    update_data = ans.model_dump(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    for key, value in update_data.items():
        setattr(db_ans, key, value)
    
    db.commit()
    db.refresh(db_ans)
    return db_ans

@router.delete("/{ans_sn}")
def delete_ans(
    ans_sn: int,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_ans = db.query(SysAnsInfo).filter(SysAnsInfo.ANS_SN == ans_sn).first()
    if db_ans is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    db_ans.DEL_YN = 'Y'
    db_ans.DEL_YN_CHG_DT = datetime.now()
    db_ans.DEL_YN_CHNRG_ID = del_id
    db_ans.DEL_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"} 