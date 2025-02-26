from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from datetime import datetime
from ..database import Base

class SystemAuthorityDetail(Base):
    __tablename__ = 'SYS_AUTHRT_DTL_INFO'

    AUTHRT_SN = Column(Integer, ForeignKey('SYS_AUTHRT_INFO.AUTHRT_SN'), primary_key=True)
    MENU_SN = Column(Integer, ForeignKey('MENU_INFO.MENU_SN'), primary_key=True)
    PRCS_SE_CD = Column(CHAR(4))
    ACTVTN_YN = Column(CHAR(1))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFCN_DT = Column(DateTime)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100)) 