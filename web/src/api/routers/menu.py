from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.MenuInfoVo import MenuInfo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/menus",
    tags=["menus"]
)

class MenuBase(BaseModel):
    menu_nm: str
    menu_price: int
    menu_desc: Optional[str] = None
    
class MenuCreate(MenuBase):
    pass

class MenuResponse(MenuBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

@router.post("/", response_model=MenuResponse)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    db_menu = MenuInfo(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.get("/", response_model=List[MenuResponse])
def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    menus = db.query(MenuInfo).offset(skip).limit(limit).all()
    return menus

@router.get("/{menu_id}", response_model=MenuResponse)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(MenuInfo).filter(MenuInfo.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
    return menu

@router.put("/{menu_id}", response_model=MenuResponse)
def update_menu(menu_id: int, menu: MenuBase, db: Session = Depends(get_db)):
    db_menu = db.query(MenuInfo).filter(MenuInfo.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
    
    for key, value in menu.dict().items():
        setattr(db_menu, key, value)
    
    db_menu.updated_at = datetime.now()
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(MenuInfo).filter(MenuInfo.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
    
    db.delete(db_menu)
    db.commit()
    return {"message": "메뉴가 삭제되었습니다"} 