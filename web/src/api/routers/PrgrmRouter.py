from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.PrgrmInfoVo import ProgramInfo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/programs",
    tags=["programs"]
)

class ProgramBase(BaseModel):
    PRGRM_SE_CD: str
    PRGRM_NM: str
    PRGRM_EXPLN: Optional[str] = None
    PRGRM_PATH_NM: str
    SORT_SN: int
    USE_YN: str = 'Y'
    RMRK_CN: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

class ProgramCreate(ProgramBase):
    pass

class ProgramResponse(ProgramBase):
    PRGRM_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ProgramResponse)
def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    db_program = ProgramInfo(
        **program.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

@router.get("/", response_model=List[ProgramResponse])
def read_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    programs = db.query(ProgramInfo).offset(skip).limit(limit).all()
    return programs

@router.get("/{program_sn}", response_model=ProgramResponse)
def read_program(program_sn: int, db: Session = Depends(get_db)):
    program = db.query(ProgramInfo).filter(ProgramInfo.PRGRM_SN == program_sn).first()
    if program is None:
        raise HTTPException(status_code=404, detail="프로그램을 찾을 수 없습니다")
    return program

@router.put("/{program_sn}", response_model=ProgramResponse)
def update_program(program_sn: int, program: ProgramBase, db: Session = Depends(get_db)):
    db_program = db.query(ProgramInfo).filter(ProgramInfo.PRGRM_SN == program_sn).first()
    if db_program is None:
        raise HTTPException(status_code=404, detail="프로그램을 찾을 수 없습니다")
    
    for key, value in program.dict(exclude_unset=True).items():
        setattr(db_program, key, value)
    
    db_program.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_program)
    return db_program

@router.delete("/{program_sn}")
def delete_program(program_sn: int, db: Session = Depends(get_db)):
    db_program = db.query(ProgramInfo).filter(ProgramInfo.PRGRM_SN == program_sn).first()
    if db_program is None:
        raise HTTPException(status_code=404, detail="프로그램을 찾을 수 없습니다")
    
    db.delete(db_program)
    db.commit()
    return {"message": "프로그램이 삭제되었습니다"} 