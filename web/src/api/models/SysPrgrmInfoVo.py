from sqlalchemy import Column, Integer, String, DateTime, CHAR
from datetime import datetime
from ..database import Base

class SystemProgram(Base):
    __tablename__ = 'SYS_PRGRM_INFO'

    PRGRM_SN = Column(Integer, primary_key=True)
    PRGRM_ID = Column(String(20))
    PRGRM_NM = Column(String(100))
    PRGRM_PATH_NM = Column(String(300))
    PRGRM_SE_CD = Column(CHAR(4))
    PRGRM_EXPLN = Column(String(4000))
    RMRK_CN = Column(String(4000))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFCN_DT = Column(DateTime)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100))
    ATCH_FILE_SN = Column(Integer)
    SORT_SN = Column(Integer) 