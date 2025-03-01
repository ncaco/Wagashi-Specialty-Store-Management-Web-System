from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SysAnsInfo(Base):
    __tablename__ = "SYS_ANS_INFO"
    
    PST_SN = Column(Integer, ForeignKey('SYS_PST_INFO.PST_SN'), nullable=False, comment="게시물일련번호")
    UP_ANS_SN = Column(Integer, ForeignKey('SYS_ANS_INFO.ANS_SN'), comment="상위답변일련번호")
    ANS_SN = Column(Integer, primary_key=True, autoincrement=True, comment="답변일련번호")
    ANS_CN = Column(String(4000), nullable=False, comment="답변내용")
    SECRT_YN = Column(CHAR(1), default='N', comment="비밀여부")
    DEL_YN = Column(CHAR(1), comment="삭제여부")
    DEL_YN_CHG_DT = Column(DateTime, comment="삭제여부변경일시")
    DEL_YN_CHNRG_ID = Column(String(20), comment="삭제여부변경자아이디")
    DEL_YN_CHNRG_NM = Column(String(100), comment="삭제여부변경자명")
    FRST_KBRDR_ID = Column(String(200), nullable=False, comment="최초입력자아이디")
    FRST_KBRDR_NM = Column(String(100), nullable=False, comment="최초입력자명")
    FRST_INPT_DT = Column(DateTime, nullable=False, default=datetime.now, comment="최초입력일시")
    LAST_MDFCN_DT = Column(DateTime, comment="최종수정일시")
    LAST_MDFR_ID = Column(String(200), comment="최종수정자아이디")
    LAST_MDFR_NM = Column(String(100), comment="최종수정자명")
    EMTCN_SN = Column(Integer, comment="이모티콘일련번호")

    # Relationships
    post = relationship("SysPstInfo", back_populates="answers")
    parent = relationship("SysAnsInfo", remote_side=[ANS_SN], backref="replies") 