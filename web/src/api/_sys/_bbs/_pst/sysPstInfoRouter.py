from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysPstInfoModel import SysPstInfo

router = APIRouter(
    prefix="/sysPstInfo",
    tags=["게시판 관련"]
)

class SysPstInfoBase(BaseModel):
    BBS_SN: int
    UP_PST_SN: Optional[int] = None
    PST_TTL: str
    PST_CN: Optional[str] = None
    PBLR_NM: Optional[str] = None
    PSWORD: Optional[str] = None
    NTC_YN: Optional[str] = 'N'
    SORT_SN: Optional[int] = None
    EXPSR_YN: Optional[str] = 'Y'
    RSVT_YN: Optional[str] = 'N'
    RSVT_DT: Optional[datetime] = None
    USE_YN: Optional[str] = 'Y'
    ATCH_FILE_ID: Optional[str] = None

class SysPstInfoCreate(SysPstInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysPstInfoUpdate(SysPstInfoBase):
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysPstInfoResponse(SysPstInfoBase):
    PST_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None
    DEL_YN: Optional[str] = None
    DEL_YN_CHG_DT: Optional[datetime] = None
    DEL_YN_CHNRG_ID: Optional[str] = None
    DEL_YN_CHNRG_NM: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=SysPstInfoResponse)
def create_pst_info(pst_info: SysPstInfoCreate, db: Session = Depends(get_db)):
    db_pst = SysPstInfo(**pst_info.dict())
    db_pst.FRST_INPT_DT = datetime.now()
    
    db.add(db_pst)
    db.commit()
    db.refresh(db_pst)
    return db_pst

@router.get("/", response_model=List[SysPstInfoResponse])
def read_pst_infos(
    skip: int = 0,
    limit: int = 100,
    bbs_sn: Optional[int] = None,
    ntc_yn: Optional[str] = None,
    expsr_yn: Optional[str] = 'Y',
    use_yn: Optional[str] = 'Y',
    del_yn: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SysPstInfo)
    if bbs_sn:
        query = query.filter(SysPstInfo.BBS_SN == bbs_sn)
    if ntc_yn:
        query = query.filter(SysPstInfo.NTC_YN == ntc_yn)
    if expsr_yn:
        query = query.filter(SysPstInfo.EXPSR_YN == expsr_yn)
    if use_yn:
        query = query.filter(SysPstInfo.USE_YN == use_yn)
    if del_yn:
        query = query.filter(SysPstInfo.DEL_YN == del_yn)
    return query.offset(skip).limit(limit).all()

@router.get("/{pst_sn}", response_model=SysPstInfoResponse)
def read_pst_info(pst_sn: int, db: Session = Depends(get_db)):
    db_pst = db.query(SysPstInfo).filter(SysPstInfo.PST_SN == pst_sn).first()
    if db_pst is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_pst

@router.put("/{pst_sn}", response_model=SysPstInfoResponse)
def update_pst_info(
    pst_sn: int,
    pst_info: SysPstInfoUpdate,
    db: Session = Depends(get_db)
):
    db_pst = db.query(SysPstInfo).filter(SysPstInfo.PST_SN == pst_sn).first()
    if db_pst is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = pst_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    for key, value in update_data.items():
        setattr(db_pst, key, value)
    
    db.commit()
    db.refresh(db_pst)
    return db_pst

@router.delete("/{pst_sn}")
def delete_pst_info(
    pst_sn: int,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_pst = db.query(SysPstInfo).filter(SysPstInfo.PST_SN == pst_sn).first()
    if db_pst is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_pst.DEL_YN = 'Y'
    db_pst.DEL_YN_CHG_DT = datetime.now()
    db_pst.DEL_YN_CHNRG_ID = del_id
    db_pst.DEL_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"} 