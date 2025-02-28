from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from database import Base, engine, init_db, get_db
from sysInfo.site.sysSiteInfoRouter import router as site_router

from pydantic import BaseModel
from datetime import datetime
from typing import List


# 데이터베이스 테이블 생성
init_db()

app = FastAPI(
    title="Fast API",
    description="Fast API",
    version="1.0.0"
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
app.include_router(site_router)

# Pydantic 모델
class AdminResponse(BaseModel):
    id: int
    username: str
    name: str
    first_login_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

@app.get("/admins/", response_model=List[AdminResponse])
def get_admins(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    admins = db.query(Base.Admin).offset(skip).limit(limit).all()
    return admins

@app.get("/admins/{admin_id}", response_model=AdminResponse)
def get_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Base.Admin).filter(Base.Admin.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="관리자를 찾을 수 없습니다")
    return admin

@app.get("/")
async def root():
    """API 상태 확인"""
    return {"status": "ok", "message": "Fast API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 