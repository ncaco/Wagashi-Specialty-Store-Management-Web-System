from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class StdTblInfo(Base):
    __tablename__ = "STD_TBL_INFO"
    
    TBL_SN = Column(Integer, primary_key=True, autoincrement=True, comment="테이블일련번호")
    TBL_LOGIC_NM = Column(String(300), nullable=False, comment="테이블논리명")
    TBL_PHYS_NM = Column(String(300), nullable=False, comment="테이블물리명")
    EXPLN = Column(String(4000), comment="설명")
    RMRK_CN = Column(String(4000), comment="비고내용")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")

    # Relationships
    columns = relationship("StdColInfo", back_populates="table")

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'comment': '표준 테이블 정보'
    } 