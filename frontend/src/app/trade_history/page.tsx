"use client";
import React, { useRef, useEffect, useState } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    LineController,
    Title,
    Tooltip,
    Legend,
    ChartOptions,
    ChartData
} from 'chart.js';

ChartJS.register(
    LineController,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

// 차트 옵션 설정
const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: '부산광역시 아파트 실거래가 추이',
            font: {
                size: 20
            }
        },
    },
    scales: {
        y: {
            title: {
                display: true,
                text: '평균 거래가(만원)'
            }
        },
        x: {
            title: {
                display: true,
                text: '월'
            }
        }
    }
};

// 초기 차트 데이터 (전체)
const initialData: ChartData<'line'> = {
    labels: ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05'],
    datasets: [
        {
            label: '부산광역시 평균 거래가',
            data: [230000, 232000, 225000, 238000, 242500],
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            tension: 0.3
        }
    ]
};

// 시군구명 상수
const districtData: string[] = ['부산진구', '사하구', '해운대구', '동래구', '남구'];

export default function TradeHistoryPage() {
    const chartRef = useRef<HTMLCanvasElement>(null);
    const chartInstanceRef = useRef<ChartJS | null>(null);
    const [selectedDistrict, setSelectedDistrict] = useState<string>('전체');
    const [data, setData] = useState<ChartData<'line'>>(initialData);

    // 차트 초기화 및 업데이트
    useEffect(() => {
        if (chartRef.current) {
            const ctx = chartRef.current.getContext('2d');
            if (ctx) {
                if (chartInstanceRef.current) {
                    chartInstanceRef.current.destroy();
                }
                chartInstanceRef.current = new ChartJS(ctx, {
                    type: 'line',
                    data: data,
                    options: options,
                });
            }
        }

        return () => {
            if (chartInstanceRef.current) {
                chartInstanceRef.current.destroy();
            }
        };
    }, [data]);

    // 시군구 선택 시 차트 데이터 업데이트
    useEffect(() => {
        if (selectedDistrict === '전체') {
            // 전체 데이터를 표시하는 로직 (예시 데이터 사용)
            const updatedData: ChartData<'line'> = {
                ...initialData,
                datasets: [
                    {
                        label: '부산광역시 평균 거래가',
                        data: [230000, 232000, 225000, 238000, 242500], // 전체 데이터 (실제 데이터로 교체 필요)
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.5)',
                        tension: 0.3
                    }
                ]
            };
            setData(updatedData);
        } else {
            // 특정 시군구 데이터를 표시하는 로직 (예시 데이터 사용)
            const districtDataMap: { [key: string]: number[] } = {
                부산진구: [45000, 46500, 44800, 47200, 48500],
                사하구: [38000, 39000, 37000, 40000, 41500],
                해운대구: [60000, 62000, 61000, 63000, 64500],
                동래구: [42000, 43500, 41000, 44500, 46000],
                남구: [50000, 51500, 49500, 53000, 54500]
            };

            const updatedData: ChartData<'line'> = {
                ...initialData,
                datasets: [
                    {
                        label: `${selectedDistrict} 평균 거래가`,
                        data: districtDataMap[selectedDistrict] || [],
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.5)',
                        tension: 0.3
                    }
                ]
            };
            setData(updatedData);
        }
    }, [selectedDistrict]);

    // 시군구 선택 핸들러
    const handleDistrictClick = (district: string) => {
        setSelectedDistrict(district);
    };

    return (
        <main className="flex">
            {/* 네비게이션 바 */}
            <nav className="w-64 bg-gray-200 p-4 overflow-auto">
                <h2 className="text-xl font-semibold mb-4">구 선택</h2>
                <ul>
                    <li className="mb-2">
                        <div
                            className={`p-2 cursor-pointer bg-gray-300 rounded ${selectedDistrict === '전체' ? 'bg-blue-500 text-white' : 'hover:bg-blue-300'
                                }`}
                            onClick={() => handleDistrictClick('전체')}
                        >
                            전체
                        </div>
                    </li>
                    {districtData.map((district) => (
                        <li key={district} className="mb-2">
                            <div
                                className={`p-2 cursor-pointer bg-gray-300 rounded ${selectedDistrict === district ? 'bg-blue-500 text-white' : 'hover:bg-blue-300'
                                    }`}
                                onClick={() => handleDistrictClick(district)}
                            >
                                {district}
                            </div>
                        </li>
                    ))}
                </ul>
            </nav>

            {/* 메인 컨텐츠 */}
            <section className="flex-1 bg-gray-100 py-12">
                <h1 className="main-title text-4xl font-bold text-center mb-4">
                    {selectedDistrict === '전체' ? '부산광역시' : `${selectedDistrict}`} 아파트 실거래가 추이
                </h1>
                <p className="sub-title text-xl text-center text-gray-700 mb-8">
                    최신 부동산 실거래가 데이터를 시각화하여 제공합니다.
                </p>
                <div className="w-full max-w-4xl h-[600px] bg-white p-8 rounded-lg shadow-lg mx-auto">
                    <canvas ref={chartRef} />
                </div>
            </section>
        </main>
    );
}