from sqlalchemy import Column, Integer, String, DateTime, CHAR
from datetime import datetime
from ..database import Base

class CertificateInfo(Base):
    __tablename__ = 'CRTFCT_INFO'

    CRTFCT_SN = Column(Integer, primary_key=True)
    CRTFCT_SE_CD = Column(CHAR(4))
    CRTFCT_KORN_NM = Column(String(100))
    CRTFCT_ENG_NM = Column(String(100))
    CRTFCT_EXPLN = Column(String(4000))
    RMRK_CN = Column(String(4000))
    ACQS_YMD = Column(CHAR(8))
    ACQS_YN = Column(CHAR(1))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100))
    LAST_MDFCN_DT = Column(DateTime) 