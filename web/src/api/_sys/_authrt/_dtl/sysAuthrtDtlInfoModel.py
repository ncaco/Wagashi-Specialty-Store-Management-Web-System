from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysAuthrtDtlInfo(Base):
    __tablename__ = "SYS_AUTHRT_DTL_INFO"
    
    AUTHRT_SN = Column(Integer, ForeignKey('SYS_AUTHRT_INFO.AUTHRT_SN'), primary_key=True, comment="권한일련번호")
    MENU_SN = Column(Integer, ForeignKey('SYS_MENU_INFO.MENU_SN'), primary_key=True, comment="메뉴일련번호")
    PRCS_SE_CD = Column(CHAR(4), primary_key=True, comment="처리구분코드")
    ACTVTN_YN = Column(CHAR(1), nullable=False, default='Y', comment="활성여부")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")

    # Relationships
    authority = relationship("SysAuthrtInfo", back_populates="details")
    menu = relationship("SysMenuInfo", back_populates="authority_details") 