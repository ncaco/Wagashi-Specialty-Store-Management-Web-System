from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class SystemPost(Base):
    __tablename__ = 'SYS_PST_INFO'

    BBS_SN = Column(Integer, ForeignKey('SYS_BBS_INFO.BBS_SN'))
    UP_PST_SN = Column(Integer)
    PST_SN = Column(Integer, primary_key=True)
    PST_TTL = Column(String(256))
    PST_CN = Column(String(4000))
    PBLR_NM = Column(String(100))
    PSWORD = Column(String(500))
    NTC_YN = Column(CHAR(1))
    SORT_SN = Column(Integer)
    EXPSR_YN = Column(CHAR(1))
    RSVT_YN = Column(CHAR(1))
    RSVT_DT = Column(DateTime)
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
    ATCH_FILE_ID = Column(String(200))

    answers = relationship("SystemAnswer", backref="post") 