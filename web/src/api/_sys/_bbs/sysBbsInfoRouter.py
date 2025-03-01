from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysBbsInfoModel import SysBbsInfo

router = APIRouter(
    prefix="/sysBbsInfo",
    tags=["게시판 관련"]
)

class SysBbsInfoBase(BaseModel):
    BBS_NM: str
    BBS_EXPLN: Optional[str] = None
    BBS_TYPE_CD: str
    RPLY_PSBLTY_YN: Optional[str] = 'Y'
    ANS_PSBLTY_YN: Optional[str] = 'Y'
    EXPSR_YN: Optional[str] = 'Y'
    SORT_SN: Optional[int] = None
    RMRK_CN: Optional[str] = None
    USE_YN: Optional[str] = 'Y'
    ATCH_FILE_SN: Optional[int] = None
    ATCH_FILE_CNT: Optional[int] = None

class SysBbsInfoCreate(SysBbsInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysBbsInfoUpdate(SysBbsInfoBase):
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysBbsInfoResponse(SysBbsInfoBase):
    BBS_SN: int
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

@router.post("/", response_model=SysBbsInfoResponse)
def create_bbs_info(bbs_info: SysBbsInfoCreate, db: Session = Depends(get_db)):
    db_bbs = SysBbsInfo(**bbs_info.dict())
    db_bbs.FRST_INPT_DT = datetime.now()
    
    db.add(db_bbs)
    db.commit()
    db.refresh(db_bbs)
    return db_bbs

@router.get("/", response_model=List[SysBbsInfoResponse])
def read_bbs_infos(
    skip: int = 0,
    limit: int = 100,
    bbs_type_cd: Optional[str] = None,
    expsr_yn: Optional[str] = 'Y',
    use_yn: Optional[str] = 'Y',
    db: Session = Depends(get_db)
):
    query = db.query(SysBbsInfo)
    if bbs_type_cd:
        query = query.filter(SysBbsInfo.BBS_TYPE_CD == bbs_type_cd)
    if expsr_yn:
        query = query.filter(SysBbsInfo.EXPSR_YN == expsr_yn)
    if use_yn:
        query = query.filter(SysBbsInfo.USE_YN == use_yn)
    return query.order_by(SysBbsInfo.SORT_SN).offset(skip).limit(limit).all()

@router.get("/{bbs_sn}", response_model=SysBbsInfoResponse)
def read_bbs_info(bbs_sn: int, db: Session = Depends(get_db)):
    db_bbs = db.query(SysBbsInfo).filter(SysBbsInfo.BBS_SN == bbs_sn).first()
    if db_bbs is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return db_bbs

@router.put("/{bbs_sn}", response_model=SysBbsInfoResponse)
def update_bbs_info(
    bbs_sn: int,
    bbs_info: SysBbsInfoUpdate,
    db: Session = Depends(get_db)
):
    db_bbs = db.query(SysBbsInfo).filter(SysBbsInfo.BBS_SN == bbs_sn).first()
    if db_bbs is None:
        raise HTTPException(status_code=404, detail="Board not found")
    
    update_data = bbs_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    if "USE_YN" in update_data and update_data["USE_YN"] != db_bbs.USE_YN:
        db_bbs.USE_YN_CHG_DT = datetime.now()
        db_bbs.USE_YN_CHNRG_ID = update_data["LAST_MDFR_ID"]
        db_bbs.USE_YN_CHNRG_NM = update_data["LAST_MDFR_NM"]
    
    for key, value in update_data.items():
        setattr(db_bbs, key, value)
    
    db.commit()
    db.refresh(db_bbs)
    return db_bbs

@router.delete("/{bbs_sn}")
def delete_bbs_info(
    bbs_sn: int,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_bbs = db.query(SysBbsInfo).filter(SysBbsInfo.BBS_SN == bbs_sn).first()
    if db_bbs is None:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # 게시물이나 메뉴에서 사용중인지 확인
    has_posts = len(db_bbs.posts) > 0
    has_menus = len(db_bbs.menus) > 0
    
    if has_posts or has_menus:
        raise HTTPException(status_code=400, detail="Cannot delete board that is being used by posts or menus")
    
    db_bbs.USE_YN = 'N'
    db_bbs.USE_YN_CHG_DT = datetime.now()
    db_bbs.USE_YN_CHNRG_ID = del_id
    db_bbs.USE_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"} 