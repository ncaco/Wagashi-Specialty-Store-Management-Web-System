'use client';

import UserLayout from '@/components/layout/UserLayout';
import Image from 'next/image';
import Link from 'next/link';

const featuredProducts = [
  {
    id: 1,
    name: '벚꽃 모찌',
    price: '3,500원',
    imageSrc: '/images/products/sakura-mochi.jpg',
    imageAlt: '벚꽃 모찌',
  },
  {
    id: 2,
    name: '말차 도라야키',
    price: '4,000원',
    imageSrc: '/images/products/matcha-dorayaki.jpg',
    imageAlt: '말차 도라야키',
  },
  {
    id: 3,
    name: '유자 대복',
    price: '3,800원',
    imageSrc: '/images/products/yuzu-daifuku.jpg',
    imageAlt: '유자 대복',
  },
  {
    id: 4,
    name: '팥 모나카',
    price: '3,200원',
    imageSrc: '/images/products/monaka.jpg',
    imageAlt: '팥 모나카',
  },
];

export default function HomePage() {
  return (
    <UserLayout>
      {/* Hero 섹션 */}
      <div className="relative">
        <div className="absolute inset-0">
          <div className="h-full w-full object-cover bg-gradient-to-r from-indigo-100 to-purple-100" />
        </div>
        <div className="relative mx-auto max-w-7xl py-24 px-6 sm:py-32 lg:px-8">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
            전통과 현대가 만나는 곳
          </h1>
          <p className="mt-6 max-w-xl text-xl text-gray-700">
            정성스럽게 만든 와가시로 일상의 달콤한 순간을 선물합니다.
            매일 아침 신선하게 만드는 수제 화과자를 만나보세요.
          </p>
          <div className="mt-10">
            <Link
              href="/menu"
              className="inline-block rounded-md border border-transparent bg-indigo-600 px-8 py-3 text-center font-medium text-white hover:bg-indigo-700"
            >
              메뉴 보기
            </Link>
          </div>
        </div>
      </div>

      {/* 추천 상품 섹션 */}
      <div className="bg-white">
        <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">이달의 추천 와가시</h2>
          <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
            {featuredProducts.map((product) => (
              <div key={product.id} className="group relative">
                <div className="aspect-h-1 aspect-w-1 w-full overflow-hidden rounded-lg bg-gray-200">
                  <Image
                    src={product.imageSrc}
                    alt={product.imageAlt}
                    width={500}
                    height={500}
                    className="h-full w-full object-cover object-center group-hover:opacity-75"
                  />
                </div>
                <div className="mt-4 flex justify-between">
                  <div>
                    <h3 className="text-sm text-gray-700">
                      <Link href={`/menu/${product.id}`}>
                        <span aria-hidden="true" className="absolute inset-0" />
                        {product.name}
                      </Link>
                    </h3>
                  </div>
                  <p className="text-sm font-medium text-gray-900">{product.price}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 매장 소개 섹션 */}
      <div className="bg-gray-50">
        <div className="mx-auto max-w-7xl py-16 px-6 sm:py-24 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900">
              정성을 담은 수제 화과자
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-500">
              매일 아침 신선한 재료로 정성스럽게 만드는 화과자로
              여러분의 일상에 달콤한 순간을 선물하고 싶습니다.
            </p>
          </div>
        </div>
      </div>
    </UserLayout>
  );
}
