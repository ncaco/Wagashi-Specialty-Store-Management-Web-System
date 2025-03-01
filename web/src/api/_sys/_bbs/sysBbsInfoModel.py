from sqlalchemy import Column, Integer, String, DateTime, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysBbsInfo(Base):
    __tablename__ = "SYS_BBS_INFO"
    
    BBS_SN = Column(Integer, primary_key=True, autoincrement=True, comment="게시판일련번호")
    BBS_NM = Column(String(256), nullable=False, comment="게시판명")
    BBS_EXPLN = Column(String(4000), comment="게시판설명")
    BBS_TYPE_CD = Column(CHAR(4), nullable=False, comment="게시판유형코드")
    RPLY_PSBLTY_YN = Column(CHAR(1), default='Y', comment="회신가능여부")
    ANS_PSBLTY_YN = Column(CHAR(1), default='Y', comment="답변가능여부")
    EXPSR_YN = Column(CHAR(1), default='Y', comment="노출여부")
    SORT_SN = Column(Integer, comment="정렬일련번호")
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
    ATCH_FILE_SN = Column(Integer, comment="첨부파일일련번호")
    ATCH_FILE_CNT = Column(Integer, comment="첨부파일수")

    # Relationships
    posts = relationship("SysPstInfo", back_populates="board")
    menus = relationship("SysMenuInfo", back_populates="board") 