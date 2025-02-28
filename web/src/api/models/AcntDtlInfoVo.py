from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from datetime import datetime
from ..database import Base

class AcntDtlInfo(Base):
    """계정 상세 정보"""
    __tablename__ = 'ACNT_DTL_INFO'

    DTL_SN = Column(Integer, primary_key=True, autoincrement=True, comment='상세일련번호')
    ACNT_SN = Column(Integer, ForeignKey('ACNT_INFO.ACNT_SN', ondelete='CASCADE'), nullable=False, comment='계정일련번호')
    KORN_FLNM = Column(String(100), comment='한글성명')
    ENG_FLNM = Column(String(100), comment='영문성명')
    HAN_FLNM = Column(String(100), comment='한자성명')
    KORN_NM = Column(String(100), comment='한글명')
    ENG_NM = Column(String(100), comment='영문명')
    HAN_NM = Column(String(100), comment='한자명')
    BRDT = Column(CHAR(8), comment='생년월일')
    SFX_RRNO_ENCPT_NM = Column(String(200), comment='뒷자리주민등록번호암호화명')
    GNDR_CD = Column(CHAR(4), comment='성별코드')
    MBL_TELNO = Column(String(11), comment='휴대전화번호')
    TELNO = Column(String(11), comment='전화번호')
    FXNO = Column(String(11), comment='팩스번호')
    NTN_CD = Column(CHAR(3), comment='국가코드')
    HOME_ADDR = Column(String(200), comment='자택주소')
    DADDR = Column(String(200), comment='상세주소')
    ZIP = Column(CHAR(5), comment='우편번호')
    PRFX_EML_AGRE_ADDR = Column(String(200), comment='앞자리이메일주소')
    SFX_EML_AGRE_ADDR = Column(String(200), comment='뒷자리이메일주소')
    PRVC_CLCT_AGRE_YN = Column(CHAR(1), nullable=False, default='N', comment='개인정보수집동의여부')
    PRVC_CLCT_AGRE_DT = Column(DateTime, comment='개인정보수집동의일시')
    TP_INFO_PVSN_AGRE_YN = Column(CHAR(1), nullable=False, default='N', comment='제3자정보제공동의여부')
    TP_INFO_PVSN_AGRE_DT = Column(DateTime, comment='제3자정보제공동의일시')
    SMS_RCPTN_AGRE_YN = Column(CHAR(1), nullable=False, default='N', comment='SMS수신동의여부')
    SMS_RCPTN_AGRE_DT = Column(DateTime, comment='SMS수신동의일시')
    EML_RCPTN_AGRE_YN = Column(CHAR(1), nullable=False, default='N', comment='이메일수신동의여부')
    EML_RCPTN_AGRE_DT = Column(DateTime, comment='이메일수신동의일시')
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment='최초입력자아이디')
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment='최초입력자명')
    FRST_INPT_DT = Column(DateTime, nullable=False, comment='최초입력일시')
    LAST_MDFR_ID = Column(String(200), comment='최종수정자아이디')
    LAST_MDFR_NM = Column(String(100), comment='최종수정자명')
    LAST_MDFCN_DT = Column(DateTime, comment='최종수정일시')