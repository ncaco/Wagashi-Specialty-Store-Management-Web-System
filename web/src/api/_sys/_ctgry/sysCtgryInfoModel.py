from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysCtgryInfo(Base):
    __tablename__ = "SYS_CTGRY_INFO"
    
    UP_CTGRY_SN = Column(Integer, ForeignKey('SYS_CTGRY_INFO.CTGRY_SN'), comment="상위범주일련번호")
    CTGRY_SN = Column(Integer, primary_key=True, autoincrement=True, comment="범주일련번호")
    CTGRY_NM = Column(String(100), nullable=False, comment="범주명")
    CTGRY_EXPLN = Column(String(4000), comment="범주설명")
    RMRK_CN = Column(String(4000), comment="비고내용")
    USE_YN = Column(CHAR(1), default='Y', comment="사용여부")
    USE_YN_CHG_DT = Column(DateTime, comment="사용여부변경일시")
    USE_YN_CHNRG_ID = Column(String(20), comment="사용여부변경자아이디")
    USE_YN_CHNRG_NM = Column(String(100), comment="사용여부변경자명")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    SORT_SN = Column(Integer, comment="정렬일련번호")

    # Relationships
    parent = relationship("SysCtgryInfo", remote_side=[CTGRY_SN], backref="children") 