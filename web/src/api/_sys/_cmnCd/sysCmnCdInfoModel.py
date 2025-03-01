from sqlalchemy import Column, String, DateTime, CHAR, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysCmnCdInfo(Base):
    __tablename__ = "SYS_CMN_CD_INFO"
    
    UP_CMN_CD = Column(CHAR(4), ForeignKey('SYS_CMN_CD_INFO.CMN_CD'), comment="상위공통코드")
    CMN_CD = Column(CHAR(4), primary_key=True, comment="공통코드")
    CD_NM = Column(String(100), nullable=False, comment="코드명")
    CD_EXPLN = Column(String(4000), comment="코드설명")
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

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('UP_CMN_CD', 'CMN_CD', name='SYS_CMN_CD_INFO_UNIQUE'),
    )

    # Relationships
    parent = relationship("SysCmnCdInfo", remote_side=[CMN_CD], backref="children") 