from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.AcntProfInfoVo import AccountProfileInfo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/account-profiles",
    tags=["account-profiles"]
)

class AccountProfileBase(BaseModel):
    ACNT_SN: int
    NICK_NM: str
    PROF_IMG_PATH_NM: Optional[str] = None
    INTRO_CN: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

class AccountProfileCreate(AccountProfileBase):
    pass

class AccountProfileResponse(AccountProfileBase):
    PROF_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=AccountProfileResponse)
def create_profile(profile: AccountProfileCreate, db: Session = Depends(get_db)):
    db_profile = AccountProfileInfo(
        **profile.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/", response_model=List[AccountProfileResponse])
def read_profiles(
    account_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(AccountProfileInfo)
    if account_sn:
        query = query.filter(AccountProfileInfo.ACNT_SN == account_sn)
    profiles = query.offset(skip).limit(limit).all()
    return profiles

@router.get("/{profile_sn}", response_model=AccountProfileResponse)
def read_profile(profile_sn: int, db: Session = Depends(get_db)):
    profile = db.query(AccountProfileInfo).filter(AccountProfileInfo.PROF_SN == profile_sn).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다")
    return profile

@router.put("/{profile_sn}", response_model=AccountProfileResponse)
def update_profile(profile_sn: int, profile: AccountProfileBase, db: Session = Depends(get_db)):
    db_profile = db.query(AccountProfileInfo).filter(AccountProfileInfo.PROF_SN == profile_sn).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다")
    
    for key, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, key, value)
    
    db_profile.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.delete("/{profile_sn}")
def delete_profile(profile_sn: int, db: Session = Depends(get_db)):
    db_profile = db.query(AccountProfileInfo).filter(AccountProfileInfo.PROF_SN == profile_sn).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다")
    
    db.delete(db_profile)
    db.commit()
    return {"message": "프로필이 삭제되었습니다"} 