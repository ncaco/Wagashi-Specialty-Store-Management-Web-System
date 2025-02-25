from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from datetime import datetime
from ..database import Base

class SystemAnswer(Base):
    __tablename__ = 'SYS_ANS_INFO'

    PST_SN = Column(Integer, ForeignKey('SYS_PST_INFO.PST_SN'))
    UP_ANS_SN = Column(Integer)
    ANS_SN = Column(Integer, primary_key=True)
    ANS_CN = Column(String(4000))
    SECRT_YN = Column(CHAR(1))
    DEL_YN = Column(CHAR(1))
    DEL_YN_CHG_DT = Column(DateTime)
    DEL_YN_CHNRG_ID = Column(String(20))
    DEL_YN_CHNRG_NM = Column(String(100))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFCN_DT = Column(DateTime)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100))
    EMTCN_SN = Column(Integer) 