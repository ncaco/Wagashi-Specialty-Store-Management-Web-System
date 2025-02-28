from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SysCmnCdInfoVo import SystemCommonCode
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/system-common-codes",
    tags=["system-common-codes"]
)

class SystemCommonCodeBase(BaseModel):
    UP_CMN_CD: Optional[str] = None
    CMN_CD: str
    CD_NM: str
    CD_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    USE_YN: str = 'Y'
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

class SystemCommonCodeCreate(SystemCommonCodeBase):
    pass

class SystemCommonCodeResponse(SystemCommonCodeBase):
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SystemCommonCodeResponse)
def create_common_code(common_code: SystemCommonCodeCreate, db: Session = Depends(get_db)):
    db_common_code = SystemCommonCode(
        **common_code.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_common_code)
    db.commit()
    db.refresh(db_common_code)
    return db_common_code

@router.get("/", response_model=List[SystemCommonCodeResponse])
def read_common_codes(
    up_cmn_cd: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SystemCommonCode)
    if up_cmn_cd:
        query = query.filter(SystemCommonCode.UP_CMN_CD == up_cmn_cd)
    common_codes = query.offset(skip).limit(limit).all()
    return common_codes

@router.get("/{cmn_cd}", response_model=SystemCommonCodeResponse)
def read_common_code(cmn_cd: str, db: Session = Depends(get_db)):
    common_code = db.query(SystemCommonCode).filter(SystemCommonCode.CMN_CD == cmn_cd).first()
    if common_code is None:
        raise HTTPException(status_code=404, detail="공통 코드를 찾을 수 없습니다")
    return common_code

@router.put("/{cmn_cd}", response_model=SystemCommonCodeResponse)
def update_common_code(cmn_cd: str, common_code: SystemCommonCodeBase, db: Session = Depends(get_db)):
    db_common_code = db.query(SystemCommonCode).filter(SystemCommonCode.CMN_CD == cmn_cd).first()
    if db_common_code is None:
        raise HTTPException(status_code=404, detail="공통 코드를 찾을 수 없습니다")
    
    for key, value in common_code.dict(exclude_unset=True).items():
        if key != "CMN_CD":  # 공통 코드 자체는 변경하지 않음
            setattr(db_common_code, key, value)
    
    db_common_code.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_common_code)
    return db_common_code

@router.delete("/{cmn_cd}")
def delete_common_code(cmn_cd: str, db: Session = Depends(get_db)):
    db_common_code = db.query(SystemCommonCode).filter(SystemCommonCode.CMN_CD == cmn_cd).first()
    if db_common_code is None:
        raise HTTPException(status_code=404, detail="공통 코드를 찾을 수 없습니다")
    
    db_common_code.USE_YN = 'N'
    db_common_code.USE_YN_CHG_DT = datetime.now()
    db.commit()
    return {"message": "공통 코드가 비활성화되었습니다"} 