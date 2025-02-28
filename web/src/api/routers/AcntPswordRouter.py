from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.AcntPswordInfoVo import AccountPasswordInfo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/account-passwords",
    tags=["account-passwords"]
)

class AccountPasswordBase(BaseModel):
    ACNT_SN: int
    SALT_ENCPT_NM: str
    PSWORD_ENCPT_NM: str
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

class AccountPasswordCreate(AccountPasswordBase):
    pass

class AccountPasswordResponse(AccountPasswordBase):
    PSWORD_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=AccountPasswordResponse)
def create_password(password: AccountPasswordCreate, db: Session = Depends(get_db)):
    db_password = AccountPasswordInfo(
        **password.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password

@router.get("/", response_model=List[AccountPasswordResponse])
def read_passwords(
    account_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(AccountPasswordInfo)
    if account_sn:
        query = query.filter(AccountPasswordInfo.ACNT_SN == account_sn)
    passwords = query.offset(skip).limit(limit).all()
    return passwords

@router.get("/{password_sn}", response_model=AccountPasswordResponse)
def read_password(password_sn: int, db: Session = Depends(get_db)):
    password = db.query(AccountPasswordInfo).filter(AccountPasswordInfo.PSWORD_SN == password_sn).first()
    if password is None:
        raise HTTPException(status_code=404, detail="비밀번호 정보를 찾을 수 없습니다")
    return password

@router.put("/{password_sn}", response_model=AccountPasswordResponse)
def update_password(password_sn: int, password: AccountPasswordBase, db: Session = Depends(get_db)):
    db_password = db.query(AccountPasswordInfo).filter(AccountPasswordInfo.PSWORD_SN == password_sn).first()
    if db_password is None:
        raise HTTPException(status_code=404, detail="비밀번호 정보를 찾을 수 없습니다")
    
    for key, value in password.dict(exclude_unset=True).items():
        setattr(db_password, key, value)
    
    db_password.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_password)
    return db_password

@router.delete("/{password_sn}")
def delete_password(password_sn: int, db: Session = Depends(get_db)):
    db_password = db.query(AccountPasswordInfo).filter(AccountPasswordInfo.PSWORD_SN == password_sn).first()
    if db_password is None:
        raise HTTPException(status_code=404, detail="비밀번호 정보를 찾을 수 없습니다")
    
    db.delete(db_password)
    db.commit()
    return {"message": "비밀번호 정보가 삭제되었습니다"} 