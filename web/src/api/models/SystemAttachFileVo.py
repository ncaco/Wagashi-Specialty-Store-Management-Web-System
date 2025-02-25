from sqlalchemy import Column, Integer, String, DateTime, CHAR
from datetime import datetime
from ..database import Base

class SystemAttachFile(Base):
    __tablename__ = 'SYS_ATCH_FILE_INFO'

    ATCH_FILE_SN = Column(Integer, primary_key=True)
    ATCH_FILE_ID = Column(String(200))
    ATCH_FILE_SE_CD = Column(CHAR(4))
    ATCH_FILE_ORGNL_NM = Column(String(300))
    ATCH_FILE_STRG_NM = Column(String(300))
    ATCH_FILE_FLDR_PATH_NM = Column(String(300))
    EXTN_NM = Column(String(5))
    ATCH_FILE_SZ = Column(Integer)
    SORT_SN = Column(Integer)
    TRGT_TBL_PHYS_NM = Column(String(300))
    TRGT_TBL_SN = Column(Integer)
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    DEL_YN = Column(CHAR(1))
    DEL_YN_CHG_DT = Column(DateTime)
    DEL_YN_CHNRG_ID = Column(String(20))
    DEL_YN_CHNRG_NM = Column(String(100)) 