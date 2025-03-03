from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .sysMenuInfoModel import SysMenuInfo

router = APIRouter(
    prefix="/sysMenuInfo",
    tags=["시스템 관련/메뉴 관련"]
)

class SysMenuInfoBase(BaseModel):
    SITE_SN: Optional[int] = None
    UP_MENU_SN: Optional[int] = None
    menu_id: Optional[str] = None
    menu_nm: Optional[str] = None
    MENU_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    SORT_SN: Optional[int] = None
    MENU_SE_CD: str
    lnkg_path_nm: Optional[str] = None
    PRGRM_SN: Optional[int] = None
    CONTS_SN: Optional[int] = None
    BBS_SN: Optional[int] = None
    expsr_yn: Optional[str] = 'Y'
    use_yn: Optional[str] = 'Y'
    ICON_SN: Optional[int] = None
    ATCH_FILE_SN: Optional[int] = None

class SysMenuInfoCreate(SysMenuInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class SysMenuInfoUpdate(SysMenuInfoBase):
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class SysMenuInfoResponse(SysMenuInfoBase):
    MENU_SN: int
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

@router.post("/", response_model=SysMenuInfoResponse)
def create_menu_info(menu_info: SysMenuInfoCreate, db: Session = Depends(get_db)):
    db_menu = SysMenuInfo(**menu_info.dict())
    db_menu.FRST_INPT_DT = datetime.now()
    
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.get("/", response_model=List[SysMenuInfoResponse])
def read_menu_infos(
    skip: int = 0,
    limit: int = 100,
    site_sn: Optional[int] = None,
    menu_id: Optional[str] = None,
    use_yn: Optional[str] = 'Y',
    db: Session = Depends(get_db)
):
    query = db.query(SysMenuInfo)
    if site_sn:
        query = query.filter(SysMenuInfo.SITE_SN == site_sn)
    if menu_id:
        query = query.filter(SysMenuInfo.menu_id == menu_id)
    if use_yn:
        query = query.filter(SysMenuInfo.use_yn == use_yn)
    return query.offset(skip).limit(limit).all()

@router.get("/{menu_sn}", response_model=SysMenuInfoResponse)
def read_menu_info(menu_sn: int, db: Session = Depends(get_db)):
    db_menu = db.query(SysMenuInfo).filter(SysMenuInfo.MENU_SN == menu_sn).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu

@router.put("/{menu_sn}", response_model=SysMenuInfoResponse)
def update_menu_info(
    menu_sn: int,
    menu_info: SysMenuInfoUpdate,
    db: Session = Depends(get_db)
):
    db_menu = db.query(SysMenuInfo).filter(SysMenuInfo.MENU_SN == menu_sn).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    update_data = menu_info.dict(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    for key, value in update_data.items():
        setattr(db_menu, key, value)
    
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.delete("/{menu_sn}")
def delete_menu_info(
    menu_sn: int,
    del_id: str = Query(..., description="삭제자 ID"),
    del_nm: str = Query(..., description="삭제자 이름"),
    db: Session = Depends(get_db)
):
    db_menu = db.query(SysMenuInfo).filter(SysMenuInfo.MENU_SN == menu_sn).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    db_menu.use_yn = 'N'
    db_menu.USE_YN_CHG_DT = datetime.now()
    db_menu.USE_YN_CHNRG_ID = del_id
    db_menu.USE_YN_CHNRG_NM = del_nm
    
    db.commit()
    return {"message": "Successfully deleted"} 