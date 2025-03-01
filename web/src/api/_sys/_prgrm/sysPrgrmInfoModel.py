from sqlalchemy import Column, Integer, String, DateTime, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysPrgrmInfo(Base):
    __tablename__ = "SYS_PRGRM_INFO"
    
    PRGRM_SN = Column(Integer, primary_key=True, autoincrement=True, comment="프로그램일련번호")
    PRGRM_ID = Column(String(20), comment="프로그램아이디")
    PRGRM_NM = Column(String(100), nullable=False, comment="프로그램명")
    PRGRM_PATH_NM = Column(String(300), comment="프로그램경로명")
    PRGRM_SE_CD = Column(CHAR(4), comment="프로그램구분코드")
    PRGRM_EXPLN = Column(String(4000), comment="프로그램설명")
    RMRK_CN = Column(String(4000), comment="비고내용")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    ATCH_FILE_SN = Column(Integer, comment="첨부파일일련번호")
    SORT_SN = Column(Integer, comment="정렬일련번호")

    # Relationships
    # 메뉴 정보와의 관계 설정
    menu = relationship("SysMenuInfo", back_populates="prgrm") 