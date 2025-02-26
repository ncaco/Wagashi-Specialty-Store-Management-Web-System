from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.orm import relationship
from ..database import Base

class AccountInfo(Base):
    __tablename__ = 'ACNT_INFO'

    ACNT_SN = Column(Integer, primary_key=True)
    ACNT_ID = Column(String(20))
    LGN_TYPE_CD = Column(CHAR(4))
    ACNT_GRD_CD = Column(CHAR(4))

    detail = relationship("AccountDetailInfo", backref="account")
    profile = relationship("AccountProfileInfo", backref="account")
    password = relationship("AccountPasswordInfo", backref="account") 