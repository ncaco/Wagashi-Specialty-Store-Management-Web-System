from sqlalchemy import Column, Integer, String, DateTime, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysAtchFileInfo(Base):
    __tablename__ = "SYS_ATCH_FILE_INFO"
    
    ATCH_FILE_SN = Column(Integer, primary_key=True, autoincrement=True, comment="첨부파일일련번호")
    ATCH_FILE_ID = Column(String(200), nullable=False, comment="첨부파일아이디")
    ATCH_FILE_SE_CD = Column(CHAR(4), comment="첨부파일구분코드(0000:첨부파일 , 0010:포스터)")
    ATCH_FILE_ORGNL_NM = Column(String(300), comment="첨부파일원본명")
    ATCH_FILE_STRG_NM = Column(String(300), comment="첨부파일저장명")
    ATCH_FILE_FLDR_PATH_NM = Column(String(300), comment="첨부파일폴더경로명")
    EXTN_NM = Column(String(5), comment="확장자명")
    ATCH_FILE_SZ = Column(Integer, comment="첨부파일크기")
    SORT_SN = Column(Integer, comment="정렬일련번호")
    TRGT_TBL_PHYS_NM = Column(String(300), comment="대상테이블물리명")
    TRGT_TBL_SN = Column(Integer, comment="대상테이블일련번호")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    DEL_YN = Column(CHAR(1), comment="삭제여부")
    DEL_YN_CHG_DT = Column(DateTime, comment="삭제여부변경일시")
    DEL_YN_CHNRG_ID = Column(String(20), comment="삭제여부변경자아이디")
    DEL_YN_CHNRG_NM = Column(String(100), comment="삭제여부변경자명")

    # Relationships
    menus = relationship("SysMenuInfo", back_populates="attachment")
    contents = relationship("SysCntsInfo", back_populates="attachment")
    boards = relationship("SysBbsInfo", back_populates="attachment") 