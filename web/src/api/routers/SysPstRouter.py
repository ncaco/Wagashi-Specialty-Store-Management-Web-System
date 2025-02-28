from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.SysPstInfoVo import SystemPost
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/system-posts",
    tags=["system-posts"]
)

class SystemPostBase(BaseModel):
    BBS_SN: int
    UP_PST_SN: Optional[int] = None
    PST_TTL: str
    PST_CN: str
    PBLR_NM: str
    PSWORD: Optional[str] = None
    NTC_YN: str = 'N'
    SORT_SN: int
    EXPSR_YN: str = 'Y'
    RSVT_YN: str = 'N'
    RSVT_DT: Optional[datetime] = None
    USE_YN: str = 'Y'
    USE_YN_CHNRG_ID: Optional[str] = None
    USE_YN_CHNRG_NM: Optional[str] = None
    DEL_YN: str = 'N'
    DEL_YN_CHNRG_ID: Optional[str] = None
    DEL_YN_CHNRG_NM: Optional[str] = None
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None
    ATCH_FILE_ID: Optional[str] = None

class SystemPostCreate(SystemPostBase):
    pass

class SystemPostResponse(SystemPostBase):
    PST_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    USE_YN_CHG_DT: Optional[datetime] = None
    DEL_YN_CHG_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=SystemPostResponse)
def create_post(post: SystemPostCreate, db: Session = Depends(get_db)):
    db_post = SystemPost(
        **post.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[SystemPostResponse])
def read_posts(
    board_sn: Optional[int] = None,
    up_post_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SystemPost)
    if board_sn:
        query = query.filter(SystemPost.BBS_SN == board_sn)
    if up_post_sn:
        query = query.filter(SystemPost.UP_PST_SN == up_post_sn)
    posts = query.offset(skip).limit(limit).all()
    return posts

@router.get("/{post_sn}", response_model=SystemPostResponse)
def read_post(post_sn: int, db: Session = Depends(get_db)):
    post = db.query(SystemPost).filter(SystemPost.PST_SN == post_sn).first()
    if post is None:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    return post

@router.put("/{post_sn}", response_model=SystemPostResponse)
def update_post(post_sn: int, post: SystemPostBase, db: Session = Depends(get_db)):
    db_post = db.query(SystemPost).filter(SystemPost.PST_SN == post_sn).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    
    for key, value in post.dict(exclude_unset=True).items():
        setattr(db_post, key, value)
    
    db_post.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_sn}")
def delete_post(post_sn: int, db: Session = Depends(get_db)):
    db_post = db.query(SystemPost).filter(SystemPost.PST_SN == post_sn).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    
    db_post.DEL_YN = 'Y'
    db_post.DEL_YN_CHG_DT = datetime.now()
    db.commit()
    return {"message": "게시물이 삭제되었습니다"} 