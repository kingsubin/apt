'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import CarouselItem from '@/types/carousel_item';

interface CarouselProps {
  items: CarouselItem[];
}

export default function Carousel({ items }: CarouselProps) {
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev === items.length - 1 ? 0 : prev + 1));
    }, 3500);

    return () => clearInterval(timer);
  }, [items.length]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
  };

  return (
    <div className="relative w-full h-[400px] bg-gray-50 rounded-lg shadow-lg overflow-hidden">
      {items.map((slide, index) => (
        <div
          key={index}
          className={`absolute w-full h-full transition-opacity duration-500 flex ${
            currentSlide === index ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <div className="w-1/3 h-full">
            <Image
              src={slide.image}
              alt={slide.name}
              width={400}
              height={400}
            />
          </div>
          <div className="w-2/3 h-full bg-white p-8 flex flex-col justify-between">
            <h2 className="text-3xl font-bold mb-6">{slide.name}</h2>

            <div className="space-y-4 text-gray-700">
              <div className="flex items-center">
                <span className="w-24 text-gray-500">거래가격</span>
                <span className="font-semibold">
                  {slide.price.toLocaleString()}만원
                </span>
              </div>

              <div className="flex items-center">
                <span className="w-24 text-gray-500">거래일</span>
                <span className="font-semibold">{formatDate(slide.date)}</span>
              </div>

              <div className="flex items-center">
                <span className="w-24 text-gray-500">전용면적</span>
                <span className="font-semibold">{slide.area}㎡</span>
              </div>

              <div className="flex items-center">
                <span className="w-24 text-gray-500">도로명주소</span>
                <span className="font-semibold">{slide.road_address}</span>
              </div>
            </div>

            <div className="mt-6 text-sm text-gray-400">※ 실거래가 기준</div>
          </div>
        </div>
      ))}
    </div>
  );
}
