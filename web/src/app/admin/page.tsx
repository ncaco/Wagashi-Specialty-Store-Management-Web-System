'use client';

import AdminLayout from '@/components/layout/admin/AdminLayout';
import { 
  UsersIcon, 
  CurrencyYenIcon, 
  ShoppingBagIcon, 
  ChartBarIcon 
} from '@heroicons/react/24/outline';

const stats = [
  {
    name: '총 직원 수',
    value: '12명',
    icon: UsersIcon,
    change: '+2.1%',
    changeType: 'positive',
  },
  {
    name: '이번 달 매출',
    value: '₩24,500,000',
    icon: CurrencyYenIcon,
    change: '+4.75%',
    changeType: 'positive',
  },
  {
    name: '상품 재고',
    value: '245개',
    icon: ShoppingBagIcon,
    change: '-3.2%',
    changeType: 'negative',
  },
  {
    name: '일일 주문량',
    value: '56건',
    icon: ChartBarIcon,
    change: '+8.1%',
    changeType: 'positive',
  },
];

export default function AdminDashboard() {
  return (
    <AdminLayout>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-xl font-semibold text-gray-900">대시보드</h1>
          <p className="mt-2 text-sm text-gray-700">
            와가시 전문점의 주요 지표와 현황을 한눈에 확인할 수 있습니다.
          </p>
        </div>
      </div>

      <div className="mt-8">
        <dl className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((item) => (
            <div
              key={item.name}
              className="relative overflow-hidden rounded-lg bg-white px-4 pt-5 pb-12 shadow sm:px-6 sm:pt-6"
            >
              <dt>
                <div className="absolute rounded-md bg-indigo-500 p-3">
                  <item.icon className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                <p className="ml-16 truncate text-sm font-medium text-gray-500">{item.name}</p>
              </dt>
              <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
                <p className="text-2xl font-semibold text-gray-900">{item.value}</p>
                <p
                  className={`ml-2 flex items-baseline text-sm font-semibold ${
                    item.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {item.change}
                </p>
              </dd>
            </div>
          ))}
        </dl>

        <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
          {/* 차트나 그래프를 추가할 수 있는 공간 */}
          <div className="h-96 rounded-lg border-2 border-dashed border-gray-200 p-4 flex items-center justify-center">
            <p className="text-gray-500">매출 추이 그래프</p>
          </div>
          <div className="h-96 rounded-lg border-2 border-dashed border-gray-200 p-4 flex items-center justify-center">
            <p className="text-gray-500">인기 상품 차트</p>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
} 