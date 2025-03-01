from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysSiteInfo(Base):
    __tablename__ = "SYS_SITE_INFO"
    
    SITE_SN = Column(Integer, primary_key=True, autoincrement=True, comment="사이트일련번호")
    SITE_ID = Column(String(20), unique=True, comment="사이트아이디")
    SITE_NM = Column(String(100), nullable=False, comment="사이트명")
    SITE_EXPLN = Column(String(4000), comment="사이트설명")
    RMRK_CN = Column(String(4000), comment="비고내용")
    USE_YN = Column(String(1), default='Y', comment="사용여부")
    USE_YN_CHG_DT = Column(DateTime, comment="사용여부변경일시")
    USE_YN_CHNRG_ID = Column(String(20), comment="사용여부변경자아이디")
    USE_YN_CHNRG_NM = Column(String(100), comment="사용여부변경자명")
    DEL_YN = Column(String(1), comment="삭제여부")
    DEL_YN_CHG_DT = Column(DateTime, comment="삭제여부변경일시")
    DEL_YN_CHNRG_ID = Column(String(20), comment="삭제여부변경자아이디")
    DEL_YN_CHNRG_NM = Column(String(100), comment="삭제여부변경자명")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    ATCH_FILE_SN = Column(Integer, comment="첨부파일일련번호")
    ICON_SN = Column(Integer, comment="아이콘일련번호")
