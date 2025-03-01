from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysCntsInfoModel import SysCntsInfo

router = APIRouter(
    prefix="/sysCntsInfo",
    tags=["콘텐츠 관련"]
)

class SysCntsInfoBase(BaseModel):
    CONTS_TTL: str
    CONTS_CN: Optional[str] = None
    CONTS_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    USE_YN: Optional[str] = 'Y'
    SORT_SN: Optional[int] = None
    ATCH_FILE_SN: Optional[int] = None

class SysCntsInfoCreate(SysCntsInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysCntsInfoUpdate(SysCntsInfoBase):
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysCntsInfoResponse(SysCntsInfoBase):
    CONTS_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=SysCntsInfoResponse)
def create_cnts_info(cnts_info: SysCntsInfoCreate, db: Session = Depends(get_db)):
    db_cnts = SysCntsInfo(**cnts_info.dict())
    db_cnts.FRST_INPT_DT = datetime.now()
    
    db.add(db_cnts)
    db.commit()
    db.refresh(db_cnts)
    return db_cnts

@router.get("/", response_model=List[SysCntsInfoResponse])
def read_cnts_infos(
    skip: int = 0,
    limit: int = 100,
    use_yn: Optional[str] = 'Y',
    db: Session = Depends(get_db)
):
    query = db.query(SysCntsInfo)
    if use_yn:
        query = query.filter(SysCntsInfo.USE_YN == use_yn)
    return query.order_by(SysCntsInfo.SORT_SN).offset(skip).limit(limit).all()

@router.get("/{conts_sn}", response_model=SysCntsInfoResponse)
def read_cnts_info(conts_sn: int, db: Session = Depends(get_db)):
    db_cnts = db.query(SysCntsInfo).filter(SysCntsInfo.CONTS_SN == conts_sn).first()
    if db_cnts is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_cnts

@router.put("/{conts_sn}", response_model=SysCntsInfoResponse)
def update_cnts_info(
    conts_sn: int,
    cnts_info: SysCntsInfoUpdate,
    db: Session = Depends(get_db)
):
    db_cnts = db.query(SysCntsInfo).filter(SysCntsInfo.CONTS_SN == conts_sn).first()
    if db_cnts is None:
        raise HTTPException(status_code=404, detail="Content not found")
    
    update_data = cnts_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    if "USE_YN" in update_data and update_data["USE_YN"] != db_cnts.USE_YN:
        db_cnts.USE_YN_CHG_DT = datetime.now()
        db_cnts.USE_YN_CHNRG_ID = update_data["LAST_MDFR_ID"]
        db_cnts.USE_YN_CHNRG_NM = update_data["LAST_MDFR_NM"]
    
    for key, value in update_data.items():
        setattr(db_cnts, key, value)
    
    db.commit()
    db.refresh(db_cnts)
    return db_cnts

@router.delete("/{conts_sn}")
def delete_cnts_info(
    conts_sn: int,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_cnts = db.query(SysCntsInfo).filter(SysCntsInfo.CONTS_SN == conts_sn).first()
    if db_cnts is None:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # 메뉴에서 사용중인지 확인
    has_menus = len(db_cnts.menus) > 0
    if has_menus:
        raise HTTPException(status_code=400, detail="Cannot delete content that is being used by menus")
    
    db_cnts.USE_YN = 'N'
    db_cnts.USE_YN_CHG_DT = datetime.now()
    db_cnts.USE_YN_CHNRG_ID = del_id
    db_cnts.USE_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"} 