# Wagashi-Specialty-Store-Management-Web-System
화과자 전문점 관리 시스템

# 기획
## 프론트엔드
- next.js
- react
- tailwindcss

## 백엔드
- fastapi

## 데이터베이스
- mariadb

## 빌드 및 배포
- 빌드 : docker-compose

## 패키지 설계
web/
├── public/                # 정적 파일 (이미지, 폰트 등)
├── src/                   # 소스 코드
│   ├── components/        # 재사용 가능한 컴포넌트
│   ├── pages/             # 페이지 컴포넌트 (Next.js의 라우팅)
│   │   ├── admin/         # 관리자 페이지 (admin)
│   │   │   ├── layout/    # admin 페이지의 레이아웃 컴포넌트
│   │   │   │   ├── Header.tsx  # admin 페이지의 헤더 컴포넌트
│   │   │   │   ├── Footer.tsx  # admin 페이지의 푸터 컴포넌트
│   │   │   │   └── ...    # 추가적인 admin 레이아웃 관련 컴포넌트
│   │   │   ├── layout.tsx  # admin 페이지의 레이아웃 컴포넌트
│   │   │   ├── index.tsx  # admin 페이지의 메인 컴포넌트
│   │   │   └── ...        # 추가적인 admin 관련 페이지
│   │   └── user/        # 사용자 페이지 (user)
│   │       ├── layout/    # user 페이지의 레이아웃 컴포넌트
│   │       │   ├── Header.tsx  # user 페이지의 헤더 컴포넌트
│   │       │   ├── Footer.tsx  # user 페이지의 푸터 컴포넌트
│   │       │   └── ...    # 추가적인 user 레이아웃 관련 컴포넌트
│   │       ├── layout.tsx  # user 페이지의 레이아웃 컴포넌트
│   │       ├── index.tsx  # user 페이지의 메인 컴포넌트
│   │       └── ...        # 추가적인 user 관련 페이지
│   ├── styles/            # 전역 CSS 및 스타일 파일
│   ├── utils/             # 유틸리티 함수
│   ├── hooks/             # 커스텀 훅
│   ├── context/           # React Context API 관련 파일
│   └── services/          # API 호출 및 서비스 관련 파일
├── .env.local             # 환경 변수 파일 (로컬 개발용)
├── .gitignore             # Git 무시 파일
├── package.json           # 패키지 정보 및 스크립트
├── README.md              # 프로젝트 설명서
└── next.config.js         # Next.js 설정 파일

#

# 분석


# 개발
1. 프레임워크 설치
```bash
npx create-next-app@latest  # Next.js 프로젝트 생성
npm install  # 패키지 설치
npm run dev  # 개발 서버 실행
```

# 평가


# 프로젝트 종료