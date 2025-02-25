'use client';

type AdminInfo = {
  name: string;
  firstLoginAt: Date;
};

// 임시 데이터 (실제로는 API나 상태관리를 통해 가져와야 함)
const adminInfo: AdminInfo = {
  name: '홍길동',
  firstLoginAt: new Date('2024-03-20T09:00:00'),
};

const formatDate = (date: Date): string => {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

export default function Header() {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      <div className="flex-1 max-w-lg">
        <div className="text-sm text-gray-500">
          최초 로그인: {formatDate(adminInfo.firstLoginAt)}
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="flex items-center">
          <button className="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            <span className="sr-only">사용자 메뉴 열기</span>
            <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
              <span className="text-sm font-medium text-gray-600">홍</span>
            </div>
            <span className="ml-3 text-sm font-medium text-gray-700">{adminInfo.name}</span>
          </button>
        </div>
      </div>
    </header>
  );
} 