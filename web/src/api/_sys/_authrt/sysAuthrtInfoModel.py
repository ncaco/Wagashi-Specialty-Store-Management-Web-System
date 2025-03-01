from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysAuthrtInfo(Base):
    __tablename__ = "SYS_AUTHRT_INFO"
    
    SITE_SN = Column(Integer, ForeignKey('SYS_SITE_INFO.SITE_SN'), nullable=False, comment="사이트일련번호")
    AUTHRT_SN = Column(Integer, primary_key=True, autoincrement=True, comment="권한일련번호")
    AUTHRT_NM = Column(String(100), comment="권한명")
    AUTHRT_GRD_CD = Column(CHAR(4), nullable=False, comment="권한등급코드")
    EXPLN = Column(String(4000), comment="설명")
    RMRK_CN = Column(String(4000), comment="비고내용")
    AUTHRT_BGNG_DT = Column(DateTime, comment="권한시작일시")
    AUTHRT_END_DT = Column(DateTime, comment="권한종료일시")
    USE_YN = Column(CHAR(1), default='Y', comment="사용여부")
    USE_YN_CHG_DT = Column(DateTime, comment="사용여부변경일시")
    USE_YN_CHNRG_ID = Column(String(20), comment="사용여부변경자아이디")
    USE_YN_CHNRG_NM = Column(String(100), comment="사용여부변경자명")
    DEL_YN = Column(CHAR(1), comment="삭제여부")
    DEL_YN_CHG_DT = Column(DateTime, comment="삭제여부변경일시")
    DEL_YN_CHNRG_ID = Column(String(20), comment="삭제여부변경자아이디")
    DEL_YN_CHNRG_NM = Column(String(100), comment="삭제여부변경자명")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")

    # Relationships
    site = relationship("SysSiteInfo", back_populates="authorities")
    details = relationship("SysAuthrtDtlInfo", back_populates="authority") 