from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from ..database import Base

class AccountProfileInfo(Base):
    __tablename__ = 'ACNT_PROF_INFO'

    PROF_SN = Column(Integer, primary_key=True)
    ACNT_SN = Column(Integer, ForeignKey('ACNT_INFO.ACNT_SN'))
    NICK_NM = Column(String(20))
    PROF_IMG_PATH_NM = Column(String(300))
    INTRO_CN = Column(String(4000))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100))
    LAST_MDFCN_DT = Column(DateTime) 