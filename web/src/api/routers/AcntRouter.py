from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.AcntInfoVo import AccountInfo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

class AccountBase(BaseModel):
    ACNT_ID: str
    LGN_TYPE_CD: str
    ACNT_GRD_CD: str

class AccountCreate(AccountBase):
    pass

class AccountResponse(AccountBase):
    ACNT_SN: int
    
    class Config:
        from_attributes = True

@router.post("/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = AccountInfo(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/", response_model=List[AccountResponse])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = db.query(AccountInfo).offset(skip).limit(limit).all()
    return accounts

@router.get("/{account_sn}", response_model=AccountResponse)
def read_account(account_sn: int, db: Session = Depends(get_db)):
    account = db.query(AccountInfo).filter(AccountInfo.ACNT_SN == account_sn).first()
    if account is None:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다")
    return account

@router.put("/{account_sn}", response_model=AccountResponse)
def update_account(account_sn: int, account: AccountBase, db: Session = Depends(get_db)):
    db_account = db.query(AccountInfo).filter(AccountInfo.ACNT_SN == account_sn).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다")
    
    for key, value in account.dict().items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

@router.delete("/{account_sn}")
def delete_account(account_sn: int, db: Session = Depends(get_db)):
    db_account = db.query(AccountInfo).filter(AccountInfo.ACNT_SN == account_sn).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다")
    
    db.delete(db_account)
    db.commit()
    return {"message": "계정이 삭제되었습니다"} 