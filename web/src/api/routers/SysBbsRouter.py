from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SysBbsInfoVo import SystemBoard
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/system-boards",
    tags=["system-boards"]
)

class SystemBoardBase(BaseModel):
    BBS_NM: str
    BBS_EXPLN: Optional[str] = None
    BBS_TYPE_CD: str
    RPLY_PSBLTY_YN: str = 'Y'
    ANS_PSBLTY_YN: str = 'Y'
    EXPSR_YN: str = 'Y'
    SORT_SN: int
    RMRK_CN: Optional[str] = None
    USE_YN: str = 'Y'
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    ATCH_FILE_SN: Optional[int] = None
    ATCH_FILE_CNT: Optional[int] = None

class SystemBoardCreate(SystemBoardBase):
    pass

class SystemBoardResponse(SystemBoardBase):
    BBS_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SystemBoardResponse)
def create_board(board: SystemBoardCreate, db: Session = Depends(get_db)):
    db_board = SystemBoard(
        **board.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

@router.get("/", response_model=List[SystemBoardResponse])
def read_boards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    boards = db.query(SystemBoard).offset(skip).limit(limit).all()
    return boards

@router.get("/{board_sn}", response_model=SystemBoardResponse)
def read_board(board_sn: int, db: Session = Depends(get_db)):
    board = db.query(SystemBoard).filter(SystemBoard.BBS_SN == board_sn).first()
    if board is None:
        raise HTTPException(status_code=404, detail="게시판을 찾을 수 없습니다")
    return board

@router.put("/{board_sn}", response_model=SystemBoardResponse)
def update_board(board_sn: int, board: SystemBoardBase, db: Session = Depends(get_db)):
    db_board = db.query(SystemBoard).filter(SystemBoard.BBS_SN == board_sn).first()
    if db_board is None:
        raise HTTPException(status_code=404, detail="게시판을 찾을 수 없습니다")
    
    for key, value in board.dict(exclude_unset=True).items():
        setattr(db_board, key, value)
    
    db_board.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_board)
    return db_board

@router.delete("/{board_sn}")
def delete_board(board_sn: int, db: Session = Depends(get_db)):
    db_board = db.query(SystemBoard).filter(SystemBoard.BBS_SN == board_sn).first()
    if db_board is None:
        raise HTTPException(status_code=404, detail="게시판을 찾을 수 없습니다")
    
    db_board.USE_YN = 'N'
    db_board.USE_YN_CHG_DT = datetime.now()
    db.commit()
    return {"message": "게시판이 비활성화되었습니다"} 