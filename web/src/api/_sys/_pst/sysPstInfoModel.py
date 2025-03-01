from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysPstInfo(Base):
    __tablename__ = "SYS_PST_INFO"
    
    BBS_SN = Column(Integer, ForeignKey('SYS_BBS_INFO.BBS_SN'), nullable=False, comment="게시판일련번호")
    UP_PST_SN = Column(Integer, ForeignKey('SYS_PST_INFO.PST_SN'), comment="상위게시물일련번호")
    PST_SN = Column(Integer, primary_key=True, autoincrement=True, comment="게시물일련번호")
    PST_TTL = Column(String(256), nullable=False, comment="게시물제목")
    PST_CN = Column(String(4000), comment="게시물내용")
    PBLR_NM = Column(String(100), comment="게시자명")
    PSWORD = Column(String(500), comment="비밀번호")
    NTC_YN = Column(CHAR(1), default='N', comment="공지여부")
    SORT_SN = Column(Integer, comment="정렬일련번호")
    EXPSR_YN = Column(CHAR(1), default='Y', comment="노출여부")
    RSVT_YN = Column(CHAR(1), default='N', comment="예약여부")
    RSVT_DT = Column(DateTime, comment="예약일시")
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
    ATCH_FILE_ID = Column(String(200), comment="첨부파일아이디")

    # Relationships
    board = relationship("SysBbsInfo", back_populates="posts")
    parent = relationship("SysPstInfo", remote_side=[PST_SN], backref="replies") 