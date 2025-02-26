from sqlalchemy import Column, Integer, String, DateTime, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class SystemBoard(Base):
    __tablename__ = 'SYS_BBS_INFO'

    BBS_SN = Column(Integer, primary_key=True)
    BBS_NM = Column(String(256))
    BBS_EXPLN = Column(String(4000))
    BBS_TYPE_CD = Column(CHAR(4))
    RPLY_PSBLTY_YN = Column(CHAR(1))
    ANS_PSBLTY_YN = Column(CHAR(1))
    EXPSR_YN = Column(CHAR(1))
    SORT_SN = Column(Integer)
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
    ATCH_FILE_SN = Column(Integer)
    ATCH_FILE_CNT = Column(Integer)

    posts = relationship("SystemPost", backref="board") 