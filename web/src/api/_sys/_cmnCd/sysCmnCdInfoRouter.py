from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysCmnCdInfoModel import SysCmnCdInfo

router = APIRouter(
    prefix="/sysCmnCdInfo",
    tags=["SYS_CMN_CD_INFO"]
)

class SysCmnCdInfoBase(BaseModel):
    UP_CMN_CD: Optional[str] = None
    CMN_CD: str
    CD_NM: str
    CD_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    USE_YN: Optional[str] = 'Y'

class SysCmnCdInfoCreate(SysCmnCdInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysCmnCdInfoUpdate(SysCmnCdInfoBase):
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysCmnCdInfoResponse(SysCmnCdInfoBase):
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

@router.post("/", response_model=SysCmnCdInfoResponse)
def create_cmn_cd_info(cmn_cd_info: SysCmnCdInfoCreate, db: Session = Depends(get_db)):
    # 공통코드 중복 체크
    existing_cd = db.query(SysCmnCdInfo).filter(
        SysCmnCdInfo.UP_CMN_CD == cmn_cd_info.UP_CMN_CD,
        SysCmnCdInfo.CMN_CD == cmn_cd_info.CMN_CD
    ).first()
    if existing_cd:
        raise HTTPException(status_code=400, detail="Common code already exists")
    
    db_cmn_cd = SysCmnCdInfo(**cmn_cd_info.dict())
    db_cmn_cd.FRST_INPT_DT = datetime.now()
    
    db.add(db_cmn_cd)
    db.commit()
    db.refresh(db_cmn_cd)
    return db_cmn_cd

@router.get("/", response_model=List[SysCmnCdInfoResponse])
def read_cmn_cd_infos(
    skip: int = 0,
    limit: int = 100,
    up_cmn_cd: Optional[str] = None,
    use_yn: Optional[str] = 'Y',
    db: Session = Depends(get_db)
):
    query = db.query(SysCmnCdInfo)
    if up_cmn_cd:
        query = query.filter(SysCmnCdInfo.UP_CMN_CD == up_cmn_cd)
    if use_yn:
        query = query.filter(SysCmnCdInfo.USE_YN == use_yn)
    return query.offset(skip).limit(limit).all()

@router.get("/{cmn_cd}", response_model=SysCmnCdInfoResponse)
def read_cmn_cd_info(cmn_cd: str, db: Session = Depends(get_db)):
    db_cmn_cd = db.query(SysCmnCdInfo).filter(SysCmnCdInfo.CMN_CD == cmn_cd).first()
    if db_cmn_cd is None:
        raise HTTPException(status_code=404, detail="Common code not found")
    return db_cmn_cd

@router.put("/{cmn_cd}", response_model=SysCmnCdInfoResponse)
def update_cmn_cd_info(
    cmn_cd: str,
    cmn_cd_info: SysCmnCdInfoUpdate,
    db: Session = Depends(get_db)
):
    db_cmn_cd = db.query(SysCmnCdInfo).filter(SysCmnCdInfo.CMN_CD == cmn_cd).first()
    if db_cmn_cd is None:
        raise HTTPException(status_code=404, detail="Common code not found")
    
    # 공통코드 중복 체크 (상위코드가 변경된 경우)
    if cmn_cd_info.UP_CMN_CD != db_cmn_cd.UP_CMN_CD:
        existing_cd = db.query(SysCmnCdInfo).filter(
            SysCmnCdInfo.UP_CMN_CD == cmn_cd_info.UP_CMN_CD,
            SysCmnCdInfo.CMN_CD == cmn_cd
        ).first()
        if existing_cd:
            raise HTTPException(status_code=400, detail="Common code already exists with new parent code")
    
    update_data = cmn_cd_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    if "USE_YN" in update_data and update_data["USE_YN"] != db_cmn_cd.USE_YN:
        db_cmn_cd.USE_YN_CHG_DT = datetime.now()
        db_cmn_cd.USE_YN_CHNRG_ID = update_data["LAST_MDFR_ID"]
        db_cmn_cd.USE_YN_CHNRG_NM = update_data["LAST_MDFR_NM"]
    
    for key, value in update_data.items():
        setattr(db_cmn_cd, key, value)
    
    db.commit()
    db.refresh(db_cmn_cd)
    return db_cmn_cd

@router.delete("/{cmn_cd}")
def delete_cmn_cd_info(
    cmn_cd: str,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_cmn_cd = db.query(SysCmnCdInfo).filter(SysCmnCdInfo.CMN_CD == cmn_cd).first()
    if db_cmn_cd is None:
        raise HTTPException(status_code=404, detail="Common code not found")
    
    # 하위 코드가 있는지 확인
    has_children = db.query(SysCmnCdInfo).filter(SysCmnCdInfo.UP_CMN_CD == cmn_cd).first() is not None
    if has_children:
        raise HTTPException(status_code=400, detail="Cannot delete code with child codes")
    
    db_cmn_cd.USE_YN = 'N'
    db_cmn_cd.USE_YN_CHG_DT = datetime.now()
    db_cmn_cd.USE_YN_CHNRG_ID = del_id
    db_cmn_cd.USE_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"} 