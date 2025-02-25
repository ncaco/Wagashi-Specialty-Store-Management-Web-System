'use client';

export default function Header() {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-end px-6">
      <div className="flex items-center">
        <button className="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          <span className="sr-only">사용자 메뉴 열기</span>
          <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
            <span className="text-sm font-medium text-gray-600">관</span>
          </div>
          <span className="ml-3 text-sm font-medium text-gray-700">관리자</span>
        </button>
      </div>
    </header>
  );
} 