from sqlalchemy import Column, Integer, String, DateTime, CHAR, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class StdDomInfo(Base):
    __tablename__ = "STD_DOM_INFO"
    
    DOM_SN = Column(Integer, primary_key=True, autoincrement=True, comment="도메인일련번호")
    STD_TYPE_CD = Column(CHAR(4), nullable=False, default='0001', comment="표준유형코드")
    STD_DOM_GROUP_NM = Column(String(200), nullable=False, comment="표준도메인그룹명")
    STD_DOM_CLSF_NM = Column(String(200), nullable=False, comment="표준도메인분류명")
    STD_DOM_CD_NM = Column(String(200), nullable=False, comment="표준도메인코드명")
    STD_DOM_NM = Column(String(200), nullable=False, comment="표준도메인명")
    STD_DOM_EXPLN = Column(String(4000), comment="표준도메인설명")
    DATA_TYPE_NM = Column(String(200), comment="자료유형명")
    DATA_SZ = Column(Integer, comment="자료크기")
    DATA_DP_SZ = Column(Integer, comment="자료소수점크기")
    STRG_FORM_NM = Column(String(200), comment="저장형식명")
    EXPR_FORM_NM = Column(String(200), comment="표현형식명")
    UNIT_NM = Column(String(200), comment="단위명")
    ALLOW_VL_CN = Column(String(2000), comment="허용값내용")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")

    # Relationships
    vocabularies = relationship("StdVocabInfo", back_populates="domain")

    __table_args__ = (
        UniqueConstraint('STD_DOM_CLSF_NM', 'STD_DOM_CD_NM', name='STD_DOM_INFO_UNIQUE'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_general_ci',
            'comment': '표준 도메인 정보'
        }
    ) 