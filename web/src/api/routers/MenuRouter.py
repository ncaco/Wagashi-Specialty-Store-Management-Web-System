from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.MenuInfoVo import MenuInfoVo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/menus",
    tags=["menus"]
)

class MenuBase(BaseModel):
    UP_MENU_SN: Optional[int] = None
    SITE_SN: int
    PRGRM_SN: int
    MENU_ID: str
    MENU_NM: str
    MENU_SE_CD: str
    SORT_SN: int
    EXPSR_YN: str = 'Y'
    USE_YN: str = 'Y'
    DEL_YN: str = 'N'
    RMRK_CN: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

class MenuCreate(MenuBase):
    pass

class MenuResponse(MenuBase):
    MENU_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=MenuResponse)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    db_menu = MenuInfoVo(
        **menu.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.get("/", response_model=List[MenuResponse])
def read_menus(
    site_sn: Optional[int] = None,
    up_menu_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(MenuInfoVo)
    if site_sn:
        query = query.filter(MenuInfoVo.SITE_SN == site_sn)
    if up_menu_sn:
        query = query.filter(MenuInfoVo.UP_MENU_SN == up_menu_sn)
    menus = query.offset(skip).limit(limit).all()
    return menus

@router.get("/{menu_sn}", response_model=MenuResponse)
def read_menu(menu_sn: int, db: Session = Depends(get_db)):
    menu = db.query(MenuInfoVo).filter(MenuInfoVo.MENU_SN == menu_sn).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
    return menu

@router.put("/{menu_sn}", response_model=MenuResponse)
def update_menu(menu_sn: int, menu: MenuBase, db: Session = Depends(get_db)):
    db_menu = db.query(MenuInfoVo).filter(MenuInfoVo.MENU_SN == menu_sn).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
    
    for key, value in menu.dict(exclude_unset=True).items():
        setattr(db_menu, key, value)
    
    db_menu.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.delete("/{menu_sn}")
def delete_menu(menu_sn: int, db: Session = Depends(get_db)):
    db_menu = db.query(MenuInfoVo).filter(MenuInfoVo.MENU_SN == menu_sn).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
    
    db.delete(db_menu)
    db.commit()
    return {"message": "메뉴가 삭제되었습니다"} 