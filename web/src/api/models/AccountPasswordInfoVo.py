from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from ..database import Base

class AccountPasswordInfo(Base):
    __tablename__ = 'ACNT_PSWORD_INFO'

    PSWORD_SN = Column(Integer, primary_key=True)
    ACNT_SN = Column(Integer, ForeignKey('ACNT_INFO.ACNT_SN'))
    SALT_ENCPT_NM = Column(String(200))
    PSWORD_ENCPT_NM = Column(String(200))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100))
    LAST_MDFCN_DT = Column(DateTime) 