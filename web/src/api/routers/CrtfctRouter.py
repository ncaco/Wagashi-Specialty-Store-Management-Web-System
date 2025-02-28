from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.CrtfctInfoVo import CertificateInfo
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/certificates",
    tags=["certificates"]
)

class CertificateBase(BaseModel):
    CRTFCT_SE_CD: str
    CRTFCT_KORN_NM: str
    CRTFCT_ENG_NM: str
    CRTFCT_EXPLN: Optional[str] = None
    RMRK_CN: Optional[str] = None
    ACQS_YMD: str
    ACQS_YN: str
    FRST_KBRDR_ID: str
    FRST_KBRDR_NM: str
    LAST_MDFR_ID: Optional[str] = None
    LAST_MDFR_NM: Optional[str] = None

class CertificateCreate(CertificateBase):
    pass

class CertificateResponse(CertificateBase):
    CRTFCT_SN: int
    FRST_INPT_DT: datetime
    LAST_MDFCN_DT: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=CertificateResponse)
def create_certificate(certificate: CertificateCreate, db: Session = Depends(get_db)):
    db_certificate = CertificateInfo(
        **certificate.dict(),
        FRST_INPT_DT=datetime.now()
    )
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

@router.get("/", response_model=List[CertificateResponse])
def read_certificates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    certificates = db.query(CertificateInfo).offset(skip).limit(limit).all()
    return certificates

@router.get("/{certificate_sn}", response_model=CertificateResponse)
def read_certificate(certificate_sn: int, db: Session = Depends(get_db)):
    certificate = db.query(CertificateInfo).filter(CertificateInfo.CRTFCT_SN == certificate_sn).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail="자격증 정보를 찾을 수 없습니다")
    return certificate

@router.put("/{certificate_sn}", response_model=CertificateResponse)
def update_certificate(certificate_sn: int, certificate: CertificateBase, db: Session = Depends(get_db)):
    db_certificate = db.query(CertificateInfo).filter(CertificateInfo.CRTFCT_SN == certificate_sn).first()
    if db_certificate is None:
        raise HTTPException(status_code=404, detail="자격증 정보를 찾을 수 없습니다")
    
    for key, value in certificate.dict(exclude_unset=True).items():
        setattr(db_certificate, key, value)
    
    db_certificate.LAST_MDFCN_DT = datetime.now()
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

@router.delete("/{certificate_sn}")
def delete_certificate(certificate_sn: int, db: Session = Depends(get_db)):
    db_certificate = db.query(CertificateInfo).filter(CertificateInfo.CRTFCT_SN == certificate_sn).first()
    if db_certificate is None:
        raise HTTPException(status_code=404, detail="자격증 정보를 찾을 수 없습니다")
    
    db.delete(db_certificate)
    db.commit()
    return {"message": "자격증 정보가 삭제되었습니다"} 