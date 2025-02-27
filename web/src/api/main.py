from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .models import models
from . import database
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .routers import account, menu

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=database.engine)

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
app.include_router(account.router)
app.include_router(menu.router)

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
def get_admins(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    admins = db.query(models.Admin).offset(skip).limit(limit).all()
    return admins

@app.get("/admins/{admin_id}", response_model=AdminResponse)
def get_admin(admin_id: int, db: Session = Depends(database.get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="관리자를 찾을 수 없습니다")
    return admin

@app.get("/")
async def root():
    """API 상태 확인"""
    return {"status": "ok", "message": "Fast API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 