from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SysCntsInfoVo import SystemContent
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/system-contents",
    tags=["system-contents"]
)

class SystemContentBase(BaseModel):
    CONTS_TTL: str
    CONTS_CN: str
    CONTS_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    USE_YN: str = 'Y'
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    ATCH_FILE_SN: Optional[int] = None
    SORT_SN: Optional[int] = None

class SystemContentCreate(SystemContentBase):
    pass

class SystemContentResponse(SystemContentBase):
    CONTS_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SystemContentResponse)
def create_content(content: SystemContentCreate, db: Session = Depends(get_db)):
    db_content = SystemContent(
        **content.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

@router.get("/", response_model=List[SystemContentResponse])
def read_contents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contents = db.query(SystemContent).offset(skip).limit(limit).all()
    return contents

@router.get("/{content_sn}", response_model=SystemContentResponse)
def read_content(content_sn: int, db: Session = Depends(get_db)):
    content = db.query(SystemContent).filter(SystemContent.CONTS_SN == content_sn).first()
    if content is None:
        raise HTTPException(status_code=404, detail="컨텐츠를 찾을 수 없습니다")
    return content

@router.put("/{content_sn}", response_model=SystemContentResponse)
def update_content(content_sn: int, content: SystemContentBase, db: Session = Depends(get_db)):
    db_content = db.query(SystemContent).filter(SystemContent.CONTS_SN == content_sn).first()
    if db_content is None:
        raise HTTPException(status_code=404, detail="컨텐츠를 찾을 수 없습니다")
    
    for key, value in content.dict(exclude_unset=True).items():
        setattr(db_content, key, value)
    
    db_content.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_content)
    return db_content

@router.delete("/{content_sn}")
def delete_content(content_sn: int, db: Session = Depends(get_db)):
    db_content = db.query(SystemContent).filter(SystemContent.CONTS_SN == content_sn).first()
    if db_content is None:
        raise HTTPException(status_code=404, detail="컨텐츠를 찾을 수 없습니다")
    
    db_content.USE_YN = 'N'
    db_content.USE_YN_CHG_DT = datetime.now()
    db.commit()
    return {"message": "컨텐츠가 비활성화되었습니다"} 