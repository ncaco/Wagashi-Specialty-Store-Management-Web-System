from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from .stdColInfoModel import StdColInfo

router = APIRouter(
    prefix="/stdColInfo",
    tags=["표준 관련/표준 컬럼 관련"]
)

class StdColInfoBase(BaseModel):
    TBL_SN: int
    VOCAB_SN: Optional[int] = None
    ESNTL_YN: str = 'N'
    ATIN_YN: str = 'N'
    SORT_SN: Optional[int] = None
    RMRK_CN: Optional[str] = None

class StdColInfoCreate(StdColInfoBase):
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str

class StdColInfoUpdate(BaseModel):
    VOCAB_SN: Optional[int] = None
    ESNTL_YN: Optional[str] = None
    ATIN_YN: Optional[str] = None
    SORT_SN: Optional[int] = None
    RMRK_CN: Optional[str] = None
    LAST_MDFR_ID: str
    LAST_MDFR_NM: str

class StdColInfoResponse(StdColInfoBase):
    COL_SN: int
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    FRST_INPT_DT: datetime
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    LAST_MDFCN_DT: Optional[datetime] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=StdColInfoResponse)
def create_column(column: StdColInfoCreate, db: Session = Depends(get_db)):
    db_column = StdColInfo(**column.model_dump())
    try:
        db.add(db_column)
        db.commit()
        db.refresh(db_column)
        return db_column
    except Exception as e:
        db.rollback()
        if "std_col_info_ibfk_1" in str(e):
            raise HTTPException(status_code=400, detail="유효하지 않은 테이블 정보입니다")
        if "std_col_info_ibfk_2" in str(e):
            raise HTTPException(status_code=400, detail="유효하지 않은 용어 정보입니다")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[StdColInfoResponse])
def read_columns(
    skip: int = 0,
    limit: int = 100,
    tbl_sn: Optional[int] = None,
    vocab_sn: Optional[int] = None,
    esntl_yn: Optional[str] = None,
    atin_yn: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(StdColInfo)
    if tbl_sn:
        query = query.filter(StdColInfo.TBL_SN == tbl_sn)
    if vocab_sn:
        query = query.filter(StdColInfo.VOCAB_SN == vocab_sn)
    if esntl_yn:
        query = query.filter(StdColInfo.ESNTL_YN == esntl_yn)
    if atin_yn:
        query = query.filter(StdColInfo.ATIN_YN == atin_yn)
    
    if tbl_sn:  # 테이블별 정렬 순서 적용
        query = query.order_by(StdColInfo.SORT_SN.asc())
    
    return query.offset(skip).limit(limit).all()

@router.get("/{col_sn}", response_model=StdColInfoResponse)
def read_column(col_sn: int, db: Session = Depends(get_db)):
    db_column = db.query(StdColInfo).filter(StdColInfo.COL_SN == col_sn).first()
    if db_column is None:
        raise HTTPException(status_code=404, detail="컬럼을 찾을 수 없습니다")
    return db_column

@router.put("/{col_sn}", response_model=StdColInfoResponse)
def update_column(col_sn: int, column: StdColInfoUpdate, db: Session = Depends(get_db)):
    db_column = db.query(StdColInfo).filter(StdColInfo.COL_SN == col_sn).first()
    if db_column is None:
        raise HTTPException(status_code=404, detail="컬럼을 찾을 수 없습니다")
    
    update_data = column.model_dump(exclude_unset=True)
    update_data["LAST_MDFCN_DT"] = datetime.now()
    
    try:
        for key, value in update_data.items():
            setattr(db_column, key, value)
        db.commit()
        db.refresh(db_column)
        return db_column
    except Exception as e:
        db.rollback()
        if "std_col_info_ibfk_2" in str(e):
            raise HTTPException(status_code=400, detail="유효하지 않은 용어 정보입니다")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/sort/{tbl_sn}", response_model=List[StdColInfoResponse])
def update_column_sort(
    tbl_sn: int,
    col_sns: List[int],
    last_mdfr_id: str = Query(..., description="수정자 ID"),
    last_mdfr_nm: str = Query(..., description="수정자 이름"),
    db: Session = Depends(get_db)
):
    try:
        for idx, col_sn in enumerate(col_sns, 1):
            db_column = db.query(StdColInfo).filter(
                StdColInfo.TBL_SN == tbl_sn,
                StdColInfo.COL_SN == col_sn
            ).first()
            if db_column:
                db_column.SORT_SN = idx
                db_column.LAST_MDFR_ID = last_mdfr_id
                db_column.LAST_MDFR_NM = last_mdfr_nm
                db_column.LAST_MDFCN_DT = datetime.now()
        
        db.commit()
        return db.query(StdColInfo).filter(
            StdColInfo.TBL_SN == tbl_sn
        ).order_by(StdColInfo.SORT_SN.asc()).all()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) 