from sqlalchemy import Column, Integer, String, DateTime, CHAR, Text, Numeric
from datetime import datetime
from database import Base

class StdWdInfo(Base):
    __tablename__ = "STD_WD_INFO"
    
    WD_SN = Column(Integer, primary_key=True, autoincrement=True, comment="단어일련번호")
    STD_TYPE_CD = Column(CHAR(4), nullable=False, default='0001', comment="표준유형코드")
    KORN_NM = Column(String(100), nullable=False, unique=True, comment="한글명")
    ENG_ABBR_NM = Column(String(200), nullable=False, unique=True, comment="영문약어명")
    ENG_NM = Column(String(100), nullable=False, comment="영문명")
    WD_EXPLN = Column(String(4000), comment="단어설명")
    FORM_WD_YN = Column(CHAR(1), nullable=False, default='N', comment="형식단어여부")
    DOM_CLSF_NM = Column(String(200), comment="도메인분류명")
    SYM_LST = Column(Text, comment="이음동의어목록")
    PROH_WD_LST = Column(Text, comment="금칙단어목록")
    WD_VER_NO = Column(Numeric(10,1), comment="단어버전번호")
    STTS_NM = Column(String(200), comment="상태명")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시") 