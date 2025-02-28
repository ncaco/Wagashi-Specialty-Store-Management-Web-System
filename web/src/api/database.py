from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
import os

load_dotenv()

# 환경변수에서 데이터베이스 접속 정보 가져오기
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# MySQL 연결 URL (PyMySQL 사용)
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 데이터베이스 URL 설정
DATABASE_URL = SQLALCHEMY_DATABASE_URL

# 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # 커넥션 풀 크기
    max_overflow=10,  # 추가로 생성 가능한 커넥션 수
    pool_timeout=30,  # 커넥션 타임아웃 (초)
    pool_recycle=1800,  # 커넥션 재사용 시간 (초)
    poolclass=QueuePool,  # 커넥션 풀 클래스
    echo=False  # SQL 로깅 여부
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 기본 클래스 생성
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 초기화 함수
def init_db():
    Base.metadata.create_all(bind=engine) 