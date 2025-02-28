from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SysAtchFileInfoVo import SysAtchFileInfoVo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/system-attachments",
    tags=["system-attachments"]
)

class SystemAttachmentBase(BaseModel):
    ATCH_FILE_ID: str
    ATCH_FILE_SE_CD: str
    ATCH_FILE_ORGNL_NM: str
    ATCH_FILE_STRG_NM: str
    ATCH_FILE_FLDR_PATH_NM: str
    EXTN_NM: str
    ATCH_FILE_SZ: int
    SORT_SN: int
    TRGT_TBL_PHYS_NM: str
    TRGT_TBL_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    DEL_YN: str = 'N'
    DEL_YN_CHNRG_ID: Optional[str] = None
    DEL_YN_CHNRG_NM: Optional[str] = None

class SystemAttachmentCreate(SystemAttachmentBase):
    pass

class SystemAttachmentResponse(SystemAttachmentBase):
    ATCH_FILE_SN: int
    FRST_INPT_DT: datetime
    DEL_YN_CHG_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SystemAttachmentResponse)
def create_attachment(attachment: SystemAttachmentCreate, db: Session = Depends(get_db)):
    db_attachment = SysAtchFileInfoVo(
        **attachment.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

@router.get("/", response_model=List[SystemAttachmentResponse])
def read_attachments(
    target_table: Optional[str] = None,
    target_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SysAtchFileInfoVo)
    if target_table:
        query = query.filter(SysAtchFileInfoVo.TRGT_TBL_PHYS_NM == target_table)
    if target_sn:
        query = query.filter(SysAtchFileInfoVo.TRGT_TBL_SN == target_sn)
    attachments = query.offset(skip).limit(limit).all()
    return attachments

@router.get("/{attachment_sn}", response_model=SystemAttachmentResponse)
def read_attachment(attachment_sn: int, db: Session = Depends(get_db)):
    attachment = db.query(SysAtchFileInfoVo).filter(SysAtchFileInfoVo.ATCH_FILE_SN == attachment_sn).first()
    if attachment is None:
        raise HTTPException(status_code=404, detail="첨부 파일을 찾을 수 없습니다")
    return attachment

@router.put("/{attachment_sn}", response_model=SystemAttachmentResponse)
def update_attachment(attachment_sn: int, attachment: SystemAttachmentBase, db: Session = Depends(get_db)):
    db_attachment = db.query(SysAtchFileInfoVo).filter(SysAtchFileInfoVo.ATCH_FILE_SN == attachment_sn).first()
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="첨부 파일을 찾을 수 없습니다")
    
    for key, value in attachment.dict(exclude_unset=True).items():
        setattr(db_attachment, key, value)
    
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

@router.delete("/{attachment_sn}")
def delete_attachment(attachment_sn: int, db: Session = Depends(get_db)):
    db_attachment = db.query(SysAtchFileInfoVo).filter(SysAtchFileInfoVo.ATCH_FILE_SN == attachment_sn).first()
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="첨부 파일을 찾을 수 없습니다")
    
    db_attachment.DEL_YN = 'Y'
    db_attachment.DEL_YN_CHG_DT = datetime.now()
    db.commit()
    return {"message": "첨부 파일이 삭제되었습니다"} 