'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  HomeIcon, 
  UserGroupIcon, 
  ShoppingBagIcon,
  CogIcon,
  QuestionMarkCircleIcon
} from '@heroicons/react/24/outline';

const menuItems = [
  { name: '개요', href: '/admin', icon: HomeIcon },
  { name: '직원 관리', href: '/admin/employees', icon: UserGroupIcon },
  { name: '상품 관리', href: '/admin/products', icon: ShoppingBagIcon },
  { name: '설정', href: '/admin/settings', icon: CogIcon },
  { name: '도움말', href: '/admin/help', icon: QuestionMarkCircleIcon },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 bg-white border-r border-gray-200">
      <div className="h-16 flex items-center px-6 border-b border-gray-200">
        <h1 className="text-xl font-semibold text-indigo-600">와가시</h1>
      </div>
      <nav className="mt-5 px-3">
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center px-3 py-2 rounded-md mb-1 text-sm font-medium ${
                isActive
                  ? 'bg-indigo-50 text-indigo-600'
                  : 'text-gray-700 hover:bg-gray-50'
              }`}
            >
              <item.icon className="h-5 w-5 mr-3" />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </div>
  );
} 