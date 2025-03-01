from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysMenuInfo(Base):
    __tablename__ = "SYS_MENU_INFO"
    
    SITE_SN = Column(Integer, ForeignKey('SYS_SITE_INFO.SITE_SN'), comment="사이트일련번호")
    UP_MENU_SN = Column(Integer, ForeignKey('SYS_MENU_INFO.MENU_SN'), comment="상위메뉴일련번호")
    MENU_SN = Column(Integer, primary_key=True, autoincrement=True, comment="메뉴일련번호")
    MENU_ID = Column(String(255), unique=True)
    MENU_NM = Column(String(255))
    MENU_EXPLN = Column(String(4000), comment="메뉴설명")
    RMRK_CN = Column(String(4000), comment="비고내용")
    SORT_SN = Column(Integer, comment="정렬일련번호")
    MENU_SE_CD = Column(CHAR(4), nullable=False, comment="메뉴구분코드")
    LNKG_PATH_NM = Column(String(255))
    PRGRM_SN = Column(Integer, ForeignKey('SYS_PRGRM_INFO.PRGRM_SN'), comment="프로그램일련번호")
    CONTS_SN = Column(Integer, ForeignKey('SYS_CNTS_INFO.CONTS_SN'), comment="콘텐츠일련번호")
    BBS_SN = Column(Integer, ForeignKey('SYS_BBS_INFO.BBS_SN'), comment="게시판일련번호")
    EXPSR_YN = Column(String(255))
    USE_YN = Column(String(255))
    USE_YN_CHG_DT = Column(DateTime, comment="사용여부변경일시")
    USE_YN_CHNRG_ID = Column(String(20), comment="사용여부변경자아이디")
    USE_YN_CHNRG_NM = Column(String(100), comment="사용여부변경자명")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    ICON_SN = Column(Integer, comment="아이콘일련번호")
    ATCH_FILE_SN = Column(Integer, comment="첨부파일일련번호")

    # Relationships
    # 사이트 정보와의 관계 설정
    site = relationship("SysSiteInfo", back_populates="menu")
    # 메뉴의 계층 구조를 위한 자기 참조 관계 설정 (상위-하위 메뉴)
    menu = relationship("SysMenuInfo", remote_side=[MENU_SN], backref="children")
    # 프로그램 정보와의 관계 설정
    prgrm = relationship("SysPrgrmInfo", back_populates="menu")
    # 콘텐츠 정보와의 관계 설정
    cnts = relationship("SysCntsInfo", back_populates="menu")
    # 게시판 정보와의 관계 설정
    bbs = relationship("SysBbsInfo", back_populates="menu")