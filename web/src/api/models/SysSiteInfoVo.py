from sqlalchemy import Column, Integer, String, DateTime, CHAR
from datetime import datetime
from ..database import Base

class SystemSite(Base):
    __tablename__ = 'SYS_SITE_INFO'

    SITE_SN = Column(Integer, primary_key=True)
    SITE_ID = Column(String(20))
    SITE_NM = Column(String(100))
    SITE_EXPLN = Column(String(4000))
    RMRK_CN = Column(String(4000))
    USE_YN = Column(CHAR(1))
    USE_YN_CHG_DT = Column(DateTime)
    USE_YN_CHNRG_ID = Column(String(20))
    USE_YN_CHNRG_NM = Column(String(100))
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
    ATCH_FILE_SN = Column(Integer)
    ICON_SN = Column(Integer) 