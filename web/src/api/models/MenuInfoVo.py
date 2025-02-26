from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from datetime import datetime
from ..database import Base

class MenuInfoVo(Base):
    __tablename__ = 'MENU_INFO'

    MENU_SN = Column(Integer, primary_key=True)
    UP_MENU_SN = Column(Integer)
    SITE_SN = Column(Integer, ForeignKey('SITE_INFO.SITE_SN'))
    PRGRM_SN = Column(Integer, ForeignKey('PRGRM_INFO.PRGRM_SN'))
    MENU_ID = Column(String(200))
    MENU_NM = Column(String(100))
    MENU_SE_CD = Column(CHAR(4))
    SORT_SN = Column(Integer)
    EXPSR_YN = Column(CHAR(1))
    USE_YN = Column(CHAR(1))
    DEL_YN = Column(CHAR(1))
    RMRK_CN = Column(String(4000))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100))
    LAST_MDFCN_DT = Column(DateTime) 