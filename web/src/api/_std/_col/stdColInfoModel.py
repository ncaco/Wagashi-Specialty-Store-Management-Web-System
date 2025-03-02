from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class StdColInfo(Base):
    __tablename__ = "STD_COL_INFO"
    
    TBL_SN = Column(Integer, ForeignKey('STD_TBL_INFO.TBL_SN'), nullable=False, comment="테이블일련번호")
    COL_SN = Column(Integer, primary_key=True, autoincrement=True, comment="컬럼일련번호")
    VOCAB_SN = Column(Integer, ForeignKey('STD_VOCAB_INFO.VOCAB_SN'), comment="용어일련번호")
    ESNTL_YN = Column(CHAR(1), nullable=False, default='N', comment="필수여부")
    ATIN_YN = Column(CHAR(1), nullable=False, default='N', comment="자동증가여부")
    SORT_SN = Column(Integer, comment="정렬일련번호")
    RMRK_CN = Column(String(4000), comment="비고내용")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")

    # Relationships
    table = relationship("StdTblInfo", back_populates="columns")
    vocabulary = relationship("StdVocabInfo", back_populates="columns")

    __table_args__ = (
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_general_ci',
            'comment': '표준 컬럼 정보'
        }
    )