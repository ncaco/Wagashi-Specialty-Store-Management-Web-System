from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import uuid
from pydantic import BaseModel
from database import get_db
from .sysAtchFileInfoModel import SysAtchFileInfo

router = APIRouter(
    prefix="/sysAtchFileInfo",
    tags=["시스템 관련/첨부파일 관리"]
)

class SysAtchFileInfoBase(BaseModel):
    ATCH_FILE_ID: str
    ATCH_FILE_SE_CD: Optional[str] = None
    ATCH_FILE_ORGNL_NM: Optional[str] = None
    ATCH_FILE_STRG_NM: Optional[str] = None
    ATCH_FILE_FLDR_PATH_NM: Optional[str] = None
    EXTN_NM: Optional[str] = None
    ATCH_FILE_SZ: Optional[int] = None
    SORT_SN: Optional[int] = None
    TRGT_TBL_PHYS_NM: Optional[str] = None
    TRGT_TBL_SN: Optional[int] = None
    DEL_YN: Optional[str] = None

class SysAtchFileInfoCreate(SysAtchFileInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysAtchFileInfoResponse(SysAtchFileInfoBase):
    ATCH_FILE_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    DEL_YN_CHG_DT: Optional[datetime] = None
    DEL_YN_CHNRG_ID: Optional[str] = None
    DEL_YN_CHNRG_NM: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/upload", response_model=SysAtchFileInfoResponse)
async def upload_file(
    file: UploadFile = File(...),
    atch_file_se_cd: Optional[str] = None,
    trgt_tbl_phys_nm: Optional[str] = None,
    trgt_tbl_sn: Optional[int] = None,
    sort_sn: Optional[int] = None,
    frst_kbrdr_id: str = Query(..., description="등록자 ID"),
    frst_kbrdr_nm: str = Query(..., description="등록자 이름"),
    db: Session = Depends(get_db)
):
    # 파일 저장 경로 설정
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # 파일 정보 추출
    file_ext = os.path.splitext(file.filename)[1]
    storage_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, storage_filename)
    
    # 파일 저장
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # DB 저장
    db_file = SysAtchFileInfo(
        ATCH_FILE_ID=str(uuid.uuid4()),
        ATCH_FILE_SE_CD=atch_file_se_cd,
        ATCH_FILE_ORGNL_NM=file.filename,
        ATCH_FILE_STRG_NM=storage_filename,
        ATCH_FILE_FLDR_PATH_NM=upload_dir,
        EXTN_NM=file_ext.lstrip('.'),
        ATCH_FILE_SZ=len(content),
        SORT_SN=sort_sn,
        TRGT_TBL_PHYS_NM=trgt_tbl_phys_nm,
        TRGT_TBL_SN=trgt_tbl_sn,
        FRST_KBRDR_ID=frst_kbrdr_id,
        FRST_KBRDR_NM=frst_kbrdr_nm,
        FRST_INPT_DT=datetime.now()
    )
    
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@router.get("/", response_model=List[SysAtchFileInfoResponse])
def read_atch_file_infos(
    skip: int = 0,
    limit: int = 100,
    atch_file_id: Optional[str] = None,
    trgt_tbl_phys_nm: Optional[str] = None,
    trgt_tbl_sn: Optional[int] = None,
    del_yn: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SysAtchFileInfo)
    if atch_file_id:
        query = query.filter(SysAtchFileInfo.ATCH_FILE_ID == atch_file_id)
    if trgt_tbl_phys_nm:
        query = query.filter(SysAtchFileInfo.TRGT_TBL_PHYS_NM == trgt_tbl_phys_nm)
    if trgt_tbl_sn:
        query = query.filter(SysAtchFileInfo.TRGT_TBL_SN == trgt_tbl_sn)
    if del_yn:
        query = query.filter(SysAtchFileInfo.DEL_YN == del_yn)
    return query.order_by(SysAtchFileInfo.SORT_SN).offset(skip).limit(limit).all()

@router.get("/{atch_file_sn}", response_model=SysAtchFileInfoResponse)
def read_atch_file_info(atch_file_sn: int, db: Session = Depends(get_db)):
    db_file = db.query(SysAtchFileInfo).filter(SysAtchFileInfo.ATCH_FILE_SN == atch_file_sn).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@router.delete("/{atch_file_sn}")
def delete_atch_file_info(
    atch_file_sn: int,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_file = db.query(SysAtchFileInfo).filter(SysAtchFileInfo.ATCH_FILE_SN == atch_file_sn).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # 물리적 파일 삭제
    file_path = os.path.join(db_file.ATCH_FILE_FLDR_PATH_NM, db_file.ATCH_FILE_STRG_NM)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # DB 정보 업데이트
    db_file.DEL_YN = 'Y'
    db_file.DEL_YN_CHG_DT = datetime.now()
    db_file.DEL_YN_CHNRG_ID = del_id
    db_file.DEL_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"} 