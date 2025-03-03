from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from database import Base, engine, init_db, get_db

# 라우터 등록
## 표준 정보 라우터
from _std._col.stdColInfoRouter import router as stdColInfoRouter
from _std._dom.stdDomInfoRouter import router as stdDomInfoRouter
from _std._tbl.stdTblInfoRouter import router as stdTblInfoRouter
from _std._vocab.stdVocabInfoRouter import router as stdVocabInfoRouter
from _std._wd.stdWdInfoRouter import router as stdWdInfoRouter

## 시스템 정보 라우터
from _sys._atchFile.sysAtchFileInfoRouter import router as sysAtchFileInfoRouter
from _sys._authrt.sysAuthrtInfoRouter import router as sysAuthrtInfoRouter
from _sys._authrt._dtl.sysAuthrtDtlInfoRouter import router as sysAuthrtDtlInfoRouter
from _sys._bbs._ans.sysAnsInfoRouter import router as sysAnsInfoRouter
from _sys._bbs._pst.sysPstInfoRouter import router as sysPstInfoRouter
from _sys._bbs.sysBbsInfoRouter import router as sysBbsInfoRouter
from _sys._cmnCd.sysCmnCdInfoRouter import router as sysCmnCdInfoRouter
from _sys._cnts.sysCntsInfoRouter import router as sysCntsInfoRouter
from _sys._ctgry.sysCtgryInfoRouter import router as sysCtgryInfoRouter
from _sys._menu.sysMenuInfoRouter import router as sysMenuInfoRouter
from _sys._prgrm.sysPrgrmInfoRouter import router as sysPrgrmInfoRouter
from _sys._site.sysSiteInfoRouter import router as sysSiteInfoRouter

from pydantic import BaseModel
from datetime import datetime
from typing import List


# 데이터베이스 테이블 생성
init_db()

app = FastAPI(
    title="와가시 전문점 관리 시스템 API",
    description="Fast API",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
## 표준 정보 라우터
app.include_router(stdColInfoRouter)
app.include_router(stdDomInfoRouter)
app.include_router(stdTblInfoRouter)
app.include_router(stdVocabInfoRouter)
app.include_router(stdWdInfoRouter)

## 시스템 정보 라우터
app.include_router(sysAtchFileInfoRouter)
app.include_router(sysAuthrtInfoRouter)
app.include_router(sysAuthrtDtlInfoRouter)
app.include_router(sysAnsInfoRouter)
app.include_router(sysPstInfoRouter)
app.include_router(sysBbsInfoRouter)
app.include_router(sysCmnCdInfoRouter)
app.include_router(sysCntsInfoRouter)
app.include_router(sysCtgryInfoRouter)
app.include_router(sysMenuInfoRouter)
app.include_router(sysPrgrmInfoRouter)
app.include_router(sysSiteInfoRouter)

# Pydantic 모델
class AdminResponse(BaseModel):
    id: int
    username: str
    name: str
    first_login_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

@app.get("/")
async def root():
    """API 상태 확인"""
    return {"status": "ok", "message": "Fast API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 