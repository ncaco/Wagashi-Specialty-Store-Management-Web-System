from sqlalchemy import Column, Integer, String, DateTime, CHAR
from datetime import datetime
from ..database import Base

class SystemCommonCode(Base):
    __tablename__ = 'SYS_CMN_CD_INFO'

    UP_CMN_CD = Column(CHAR(4))
    CMN_CD = Column(CHAR(4), primary_key=True)
    CD_NM = Column(String(100))
    CD_EXPLN = Column(String(4000))
    RMRK_CN = Column(String(4000))
    USE_YN = Column(CHAR(1))
    USE_YN_CHG_DT = Column(DateTime)
    USE_YN_CHNRG_ID = Column(String(20))
    USE_YN_CHNRG_NM = Column(String(100))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFCN_DT = Column(DateTime)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100)) 