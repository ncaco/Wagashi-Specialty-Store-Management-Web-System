from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .stdTblInfoModel import StdTblInfo

router = APIRouter(
    prefix="/stdTblInfo",
    tags=["STD_TBL_INFO"]
)

class StdTblInfoBase(BaseModel):
    TBL_LOGIC_NM: str
    TBL_PHYS_NM: str
    EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None

class StdTblInfoCreate(StdTblInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class StdTblInfoUpdate(BaseModel):
    EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class StdTblInfoResponse(StdTblInfoBase):
    TBL_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    LAST_MDFCN_DT: Optional[datetime] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=StdTblInfoResponse)
def create_table(table: StdTblInfoCreate, db: Session = Depends(get_db)):
    db_table = StdTblInfo(**table.model_dump())
    try:
        db.add(db_table)
        db.commit()
        db.refresh(db_table)
        return db_table
    except Exception as e:
        db.rollback()
        if "STD_TBL_INFO_UNIQUE" in str(e):
            raise HTTPException(
                status_code=400, 
                detail="동일한 논리명과 물리명을 가진 테이블이 이미 존재합니다"
            )
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[StdTblInfoResponse])
def read_tables(
    skip: int = 0,
    limit: int = 100,
    tbl_logic_nm: Optional[str] = None,
    tbl_phys_nm: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(StdTblInfo)
    if tbl_logic_nm:
        query = query.filter(StdTblInfo.TBL_LOGIC_NM.like(f"%{tbl_logic_nm}%"))
    if tbl_phys_nm:
        query = query.filter(StdTblInfo.TBL_PHYS_NM.like(f"%{tbl_phys_nm}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/{tbl_sn}", response_model=StdTblInfoResponse)
def read_table(tbl_sn: int, db: Session = Depends(get_db)):
    db_table = db.query(StdTblInfo).filter(StdTblInfo.TBL_SN == tbl_sn).first()
    if db_table is None:
        raise HTTPException(status_code=404, detail="테이블을 찾을 수 없습니다")
    return db_table

@router.put("/{tbl_sn}", response_model=StdTblInfoResponse)
def update_table(tbl_sn: int, table: StdTblInfoUpdate, db: Session = Depends(get_db)):
    db_table = db.query(StdTblInfo).filter(StdTblInfo.TBL_SN == tbl_sn).first()
    if db_table is None:
        raise HTTPException(status_code=404, detail="테이블을 찾을 수 없습니다")
    
    update_data = table.model_dump(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    try:
        for key, value in update_data.items():
            setattr(db_table, key, value)
        db.commit()
        db.refresh(db_table)
        return db_table
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check/duplicate", response_model=dict)
def check_duplicate(
    tbl_logic_nm: Optional[str] = None,
    tbl_phys_nm: Optional[str] = None,
    db: Session = Depends(get_db)
):
    result = {"exists": False}
    
    if tbl_logic_nm and tbl_phys_nm:
        exists = db.query(StdTblInfo).filter(
            StdTblInfo.TBL_LOGIC_NM == tbl_logic_nm,
            StdTblInfo.TBL_PHYS_NM == tbl_phys_nm
        ).first()
        result["exists"] = exists is not None
        
    return result 