from sqlalchemy import Column, Integer, String, DateTime, CHAR, Text, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class StdVocabInfo(Base):
    __tablename__ = "STD_VOCAB_INFO"
    
    VOCAB_SN = Column(Integer, primary_key=True, autoincrement=True, comment="용어일련번호")
    STD_TYPE_CD = Column(CHAR(4), nullable=False, comment="표준유형코드")
    KORN_VOCAB_NM = Column(String(200), nullable=False, unique=True, comment="한글용어명")
    ENG_ABBR_NM = Column(String(200), nullable=False, unique=True, comment="영문약어명")
    STD_DOM_CLSF_NM = Column(String(200), nullable=False, comment="표준도메인분류명")
    STD_DOM_CD_NM = Column(String(200), nullable=False, comment="표준도메인코드명")
    VOCAB_EXPLN = Column(String(4000), comment="용어설명")
    PBADMS_STD_CD_NM = Column(String(200), comment="행정표준코드명")
    AFFL_INST_NM = Column(String(200), comment="소관기관명")
    VOCAB_SYM_LST = Column(Text, comment="용어이음동의어목록")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")

    __table_args__ = (
        ForeignKeyConstraint(
            ['STD_DOM_CLSF_NM', 'STD_DOM_CD_NM'],
            ['STD_DOM_INFO.STD_DOM_CLSF_NM', 'STD_DOM_INFO.STD_DOM_CD_NM'],
            onupdate="NO ACTION",
            ondelete="NO ACTION"
        ),
    )

    # Relationships
    domain = relationship("StdDomInfo", foreign_keys=[STD_DOM_CLSF_NM, STD_DOM_CD_NM]) 