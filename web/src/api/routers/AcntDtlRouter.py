from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.AcntDtlInfoVo import AcntDtlInfo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/acntDtlInfo",
    tags=["acntDtlInfo"]
)

class AcntDtlBase(BaseModel):
    ACNT_SN: int  # 계정일련번호
    KORN_FLNM: str  # 한글성명
    ENG_FLNM: Optional[str] = None  # 영문성명
    HAN_FLNM: Optional[str] = None  # 한자성명
    KORN_NM: Optional[str] = None  # 한글명
    ENG_NM: Optional[str] = None  # 영문명
    HAN_NM: Optional[str] = None  # 한자명
    BRDT: str  # 생년월일
    SFX_RRNO_ENCPT_NM: Optional[str] = None  # 뒷자리주민등록번호암호화명
    GNDR_CD: str  # 성별코드
    MBL_TELNO: Optional[str] = None  # 휴대전화번호
    TELNO: Optional[str] = None  # 전화번호
    FXNO: Optional[str] = None  # 팩스번호
    NTN_CD: Optional[str] = None  # 국가코드
    HOME_ADDR: Optional[str] = None  # 자택주소
    DADDR: Optional[str] = None  # 상세주소
    ZIP: Optional[str] = None  # 우편번호
    PRFX_EML_AGRE_ADDR: Optional[str] = None  # 앞자리이메일주소
    SFX_EML_AGRE_ADDR: Optional[str] = None  # 뒷자리이메일주소
    PRVC_CLCT_AGRE_YN: str = 'N'  # 개인정보수집동의여부
    PRVC_CLCT_AGRE_DT: Optional[datetime] = None  # 개인정보수집동의일시
    TP_INFO_PVSN_AGRE_YN: str = 'N'  # 제3자정보제공동의여부
    TP_INFO_PVSN_AGRE_DT: Optional[datetime] = None  # 제3자정보제공동의일시
    SMS_RCPTN_AGRE_YN: str = 'N'  # SMS수신동의여부
    SMS_RCPTN_AGRE_DT: Optional[datetime] = None  # SMS수신동의일시
    EML_RCPTN_AGRE_YN: str = 'N'  # 이메일수신동의여부
    EML_RCPTN_AGRE_DT: Optional[datetime] = None  # 이메일수신동의일시
    FRST_KBRDR_ID: str  # 최초입력자아이디
    FRST_KBRDR_NM: str  # 최초입력자명

class AcntDtlCreate(AcntDtlBase):
    pass

class AcntDtlResponse(AcntDtlBase):
    DTL_SN: int  # 상세일련번호
    FRST_INPT_DT: datetime  # 최초입력일시
    LAST_MDFR_ID: Optional[str] = None  # 최종수정자아이디
    LAST_MDFR_NM: Optional[str] = None  # 최종수정자명
    LAST_MDFCN_DT: Optional[datetime] = None  # 최종수정일시
    
    class Config:
        from_attributes = True

@router.post("/", response_model=AcntDtlResponse)
def create_account_detail(account_detail: AcntDtlCreate, db: Session = Depends(get_db)):
    db_account_detail = AcntDtlInfo(
        **account_detail.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_account_detail)
    db.commit()
    db.refresh(db_account_detail)
    return db_account_detail

@router.get("/", response_model=List[AcntDtlResponse])
def read_account_details(
    account_sn: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(AcntDtlInfo)
    
    if account_sn:
        query = query.filter(AcntDtlInfo.ACNT_SN == account_sn)
    
    account_details = query.offset(skip).limit(limit).all()
    return account_details

@router.get("/{detail_sn}", response_model=AcntDtlResponse)
def read_account_detail(detail_sn: int, db: Session = Depends(get_db)):
    account_detail = db.query(AcntDtlInfo).filter(AcntDtlInfo.DTL_SN == detail_sn).first()
    if account_detail is None:
        raise HTTPException(status_code=404, detail="계정 상세 정보를 찾을 수 없습니다")
    return account_detail

@router.put("/{detail_sn}", response_model=AcntDtlResponse)
def update_account_detail(detail_sn: int, account_detail: AcntDtlBase, db: Session = Depends(get_db)):
    db_account_detail = db.query(AcntDtlInfo).filter(AcntDtlInfo.DTL_SN == detail_sn).first()
    if db_account_detail is None:
        raise HTTPException(status_code=404, detail="계정 상세 정보를 찾을 수 없습니다")
    
    for key, value in account_detail.dict(exclude_unset=True).items():
        setattr(db_account_detail, key, value)
    
    db_account_detail.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_account_detail)
    return db_account_detail

@router.delete("/{detail_sn}")
def delete_account_detail(detail_sn: int, db: Session = Depends(get_db)):
    db_account_detail = db.query(AcntDtlInfo).filter(AcntDtlInfo.DTL_SN == detail_sn).first()
    if db_account_detail is None:
        raise HTTPException(status_code=404, detail="계정 상세 정보를 찾을 수 없습니다")
    
    db.delete(db_account_detail)
    db.commit()
    return {"message": "계정 상세 정보가 삭제되었습니다"}