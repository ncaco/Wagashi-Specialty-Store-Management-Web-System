from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class SiteInfo(Base):
    __tablename__ = 'SITE_INFO'

    SITE_SN = Column(Integer, primary_key=True)
    ACNT_SN = Column(Integer, ForeignKey('ACNT_INFO.ACNT_SN'))
    SITE_GRD_CD = Column(CHAR(4))
    SITE_ID = Column(String(20))
    SITE_NM = Column(String(100))
    RPRS_ICON_PATH_NM = Column(String(300))
    SITE_LOGO_NM = Column(String(200))
    RMRK_CN = Column(String(4000))
    FRST_KBRDR_ID = Column(String(200))
    FRST_KBRDR_NM = Column(String(100))
    FRST_INPT_DT = Column(DateTime, nullable=False)
    LAST_MDFR_ID = Column(String(200))
    LAST_MDFR_NM = Column(String(100))
    LAST_MDFCN_DT = Column(DateTime)

    menus = relationship("MenuInfo", backref="site") 