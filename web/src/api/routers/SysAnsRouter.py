from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SysAnsInfoVo import SystemAnswer
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/system-answers",
    tags=["system-answers"]
)

class SystemAnswerBase(BaseModel):
    PST_SN: int
    UP_ANS_SN: Optional[int] = None
    ANS_CN: str
    SECRT_YN: str = 'N'
    DEL_YN: str = 'N'
    DEL_YN_CHNRG_ID: Optional[str] = None
    DEL_YN_CHNRG_NM: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    EMTCN_SN: Optional[int] = None

class SystemAnswerCreate(SystemAnswerBase):
    pass

class SystemAnswerResponse(SystemAnswerBase):
    ANS_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    DEL_YN_CHG_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SystemAnswerResponse)
def create_answer(answer: SystemAnswerCreate, db: Session = Depends(get_db)):
    db_answer = SystemAnswer(
        **answer.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

@router.get("/", response_model=List[SystemAnswerResponse])
def read_answers(
    post_sn: Optional[int] = None,
    up_ans_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SystemAnswer)
    if post_sn:
        query = query.filter(SystemAnswer.PST_SN == post_sn)
    if up_ans_sn:
        query = query.filter(SystemAnswer.UP_ANS_SN == up_ans_sn)
    answers = query.offset(skip).limit(limit).all()
    return answers

@router.get("/{answer_sn}", response_model=SystemAnswerResponse)
def read_answer(answer_sn: int, db: Session = Depends(get_db)):
    answer = db.query(SystemAnswer).filter(SystemAnswer.ANS_SN == answer_sn).first()
    if answer is None:
        raise HTTPException(status_code=404, detail="답변을 찾을 수 없습니다")
    return answer

@router.put("/{answer_sn}", response_model=SystemAnswerResponse)
def update_answer(answer_sn: int, answer: SystemAnswerBase, db: Session = Depends(get_db)):
    db_answer = db.query(SystemAnswer).filter(SystemAnswer.ANS_SN == answer_sn).first()
    if db_answer is None:
        raise HTTPException(status_code=404, detail="답변을 찾을 수 없습니다")
    
    for key, value in answer.dict(exclude_unset=True).items():
        setattr(db_answer, key, value)
    
    db_answer.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_answer)
    return db_answer

@router.delete("/{answer_sn}")
def delete_answer(answer_sn: int, db: Session = Depends(get_db)):
    db_answer = db.query(SystemAnswer).filter(SystemAnswer.ANS_SN == answer_sn).first()
    if db_answer is None:
        raise HTTPException(status_code=404, detail="답변을 찾을 수 없습니다")
    
    db_answer.DEL_YN = 'Y'
    db_answer.DEL_YN_CHG_DT = datetime.now()
    db.commit()
    return {"message": "답변이 삭제되었습니다"} 