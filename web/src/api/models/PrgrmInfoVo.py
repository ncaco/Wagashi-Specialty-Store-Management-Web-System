from sqlalchemy import Column, Integer, String, DateTime, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class ProgramInfo(Base):
    __tablename__ = 'PRGRM_INFO'

    PRGRM_SN = Column(Integer, primary_key=True)
    PRGRM_SE_CD = Column(CHAR(4))
    PRGRM_NM = Column(String(200))
    PRGRM_EXPLN = Column(String(4000))
    PRGRM_PATH_NM = Column(String(300))
    SORT_SN = Column(Integer)
    USE_YN = Column(CHAR(1))
    RMRK_CN = Column(String(4000))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100))
    LAST_MDFCN_DT = Column(DateTime)

    menus = relationship("MenuInfo", backref="program") 