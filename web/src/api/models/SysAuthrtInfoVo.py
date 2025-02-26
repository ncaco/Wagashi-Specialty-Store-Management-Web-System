from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class SystemAuthority(Base):
    __tablename__ = 'SYS_AUTHRT_INFO'

    SITE_SN = Column(Integer, ForeignKey('SITE_INFO.SITE_SN'))
    AUTHRT_SN = Column(Integer, primary_key=True)
    AUTHRT_NM = Column(String(100))
    AUTHRT_GRD_CD = Column(CHAR(4))
    EXPLN = Column(String(4000))
    RMRK_CN = Column(String(4000))
    AUTHRT_BGNG_DT = Column(DateTime)
    AUTHRT_END_DT = Column(DateTime)
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

    details = relationship("SystemAuthorityDetail", backref="authority") 