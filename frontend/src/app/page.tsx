"use client";

import { useState, useEffect, useMemo } from 'react';
import ChartSection from './components/ChartSection';
interface CarouselItem {
  image: string;
  name: string;
  price: number;
  date: string;
  area: number;
  road_address: string;
}

export default function Home() {
  const [currentSlide, setCurrentSlide] = useState(0);

  // 캐러셀 데이터
  const carouselData: CarouselItem[] = [
    {
      image: "/images/1.webp",
      name: "해운대 엘시티",
      price: 250000,
      date: "2024-03-15",
      area: 84.23,
      road_address: "부산광역시 해운대구 달맞이길 30"
    },
    {
      image: "/images/2.webp",
      name: "센텀 파크뷰",
      price: 250000,
      date: "2024-03-15",
      area: 84.23,
      road_address: "부산광역시 해운대구 달맞이길 30"
    },
    {
      image: "/images/3.webp",
      name: "두산위브더제니스 센트럴사하",
      price: 250000,
      date: "2024-03-15",
      area: 84.23,
      road_address: "부산광역시 해운대구 달맞이길 30"
    },
    {
      image: "/images/4.webp",
      name: "에코델타시티 한양수자인",
      price: 250000,
      date: "2024-03-15",
      area: 84.23,
      road_address: "부산광역시 해운대구 달맞이길 30"
    },
    {
      image: "/images/5.webp",
      name: "사직하늘채 리센티아",
      price: 250000,
      date: "2024-03-15",
      area: 84.23,
      road_address: "부산광역시 해운대구 달맞이길 30"
    }
  ];

  // 차트 데이터
  const chartData = useMemo(() => [
    {
      title: "부산진구",
      value: 45000,
      change: 0.26,
      data: [44000, 44500, 44800, 45200, 45000, 45100, 45000]
    },
    {
      title: "부산서구",
      value: 38000,
      change: -0.15,
      data: [38500, 38300, 38200, 38100, 38000, 37900, 38000]
    },
    {
      title: "부산중구",
      value: 42000,
      change: 0.18,
      data: [41800, 41900, 42000, 42100, 42000, 42100, 42000]
    },
    {
      title: "부산금정구",
      value: 40000,
      change: -0.22,
      data: [40200, 40100, 40000, 39900, 39800, 39900, 40000]
    }
  ], []);

  // 자동 슬라이드 효과
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) =>
        prev === carouselData.length - 1 ? 0 : prev + 1
      );
    }, 3500);

    return () => clearInterval(timer);
  }, []);

  // 날짜 포맷팅
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
  };

  return (
    <main className="p-4">
      {/* 차트 섹션 */}
      <h1 className="text-3xl font-bold mb-4 mt-4 text-gray-800">
        부산 아파트 실거래 추이
      </h1>
      <ChartSection chartData={chartData} />

      {/* <div className="mt-8">
        <h1 className="text-2xl font-bold mb-4">최근 부산 아파트 실거래</h1>
      </div> */}

      <h1 className="text-3xl font-bold mb-4 mt-12 text-gray-800">
        최근 부산 아파트 실거래
      </h1>

      {/* 캐러셀 섹션 - 카드 형식으로 변경 */}
      <section className="mt-8">
        <div className="relative w-full h-[400px] bg-gray-50 rounded-lg shadow-lg overflow-hidden">
          {carouselData.map((slide, index) => (
            <div
              key={index}
              className={`absolute w-full h-full transition-opacity duration-500 flex ${currentSlide === index ? 'opacity-100' : 'opacity-0'
                }`}
            >
              <div className="w-1/3 h-full">
                <img
                  src={slide.image}
                  alt={slide.name}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="w-2/3 h-full bg-white p-8 flex flex-col justify-between">
                <h2 className="text-3xl font-bold mb-6">{slide.name}</h2>

                <div className="space-y-4 text-gray-700">
                  <div className="flex items-center">
                    <span className="w-24 text-gray-500">거래가격</span>
                    <span className="font-semibold">{slide.price.toLocaleString()}만원</span>
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

                <div className="mt-6 text-sm text-gray-400">
                  ※ 실거래가 기준
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}