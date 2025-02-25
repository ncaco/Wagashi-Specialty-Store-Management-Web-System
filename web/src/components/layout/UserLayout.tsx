'use client';

import { ReactNode } from 'react';
import Link from 'next/link';
import { ShoppingBagIcon } from '@heroicons/react/24/outline';

const navigation = [
  { name: '메뉴', href: '/menu' },
  { name: '매장 소개', href: '/about' },
  { name: '오시는 길', href: '/location' },
  { name: '예약', href: '/reservation' },
];

interface UserLayoutProps {
  children: ReactNode;
}

export default function UserLayout({ children }: UserLayoutProps) {
  return (
    <div className="min-h-screen bg-white">
      <header className="bg-white shadow-sm">
        <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8" aria-label="Top">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center">
              <Link href="/" className="text-2xl font-bold text-indigo-600">
                와가시
              </Link>
            </div>
            <div className="hidden md:flex md:items-center md:space-x-6">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="text-sm font-medium text-gray-700 hover:text-indigo-600"
                >
                  {item.name}
                </Link>
              ))}
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/cart"
                className="group -m-2 flex items-center p-2"
              >
                <ShoppingBagIcon
                  className="h-6 w-6 text-gray-400 group-hover:text-indigo-600"
                  aria-hidden="true"
                />
                <span className="ml-2 text-sm font-medium text-gray-700 group-hover:text-indigo-600">
                  0
                </span>
              </Link>
            </div>
          </div>
        </nav>
      </header>

      <main>{children}</main>

      <footer className="bg-white">
        <div className="mx-auto max-w-7xl px-6 py-12 md:flex md:items-center md:justify-between lg:px-8">
          <div className="mt-8 md:order-1 md:mt-0">
            <p className="text-center text-xs leading-5 text-gray-500">
              &copy; 2024 와가시. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
} 