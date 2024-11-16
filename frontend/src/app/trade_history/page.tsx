'use client';
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
  ChartData,
  BarElement,
  BarController,
} from 'chart.js';
import TradeStats from '@/types/trade-stats';

interface ApiResponse<T> {
  status: string;
  data: {
    [key: string]: T;
  }
}

ChartJS.register(
  LineController,
  BarController,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

// 시군구명 상수
const districtData: string[] = [
  '중구',
  '서구',
  '동구',
  '영도구',
  '부산진구',
  '동래구',
  '남구',
  '북구',
  '해운대구',
  '사하구',
  '금정구',
  '강서구',
  '연제구',
  '수영구',
  '사상구',
  '기장군',
];

// 기간별 차트 레이블 반환 함수
const getRangeTitle = (range: string) => {
  switch (range) {
    case '1W': return '1주';
    case '1M': return '1개월';
    case '3M': return '3개월';
    case '6M': return '6개월';
    case '1Y': return '1년';
    case '3Y': return '3년';
    default: return '1년';
  }
};

// 기간별 최대 틱 수 반환 함수
const getMaxTicksLimit = (range: string) => {
  switch (range) {
    case '1W': return 7;    // 1주일은 7개
    case '1M': return 28;   // 1개월은 28개
    case '3M': return 84;   // 3개월은 84개
    case '6M': return 168;  // 6개월은 168개
    case '1Y': return 365;  // 1년은 365개
    case '3Y': return 1095; // 3년은 1095개
    default: return 365;
  }
};

// 날짜 포맷팅 함수
const formatDate = (date: Date, range: string) => {
  switch (range) {
    case '1W':
      return `${date.getMonth() + 1}/${date.getDate()}`; // 11/20
    case '1M':
    case '3M':
      return `${date.getMonth() + 1}월 ${date.getDate()}일`; // 11월 20일
    case '6M':
    case '1Y':
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`; // 2024-03
    case '3Y':
      return `${date.getFullYear()}년 ${date.getMonth() + 1}월`; // 2024년 3월
    default:
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
  }
};

export default function TradeHistoryPage() {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstanceRef = useRef<ChartJS | null>(null);

  const [selectedDistrict, setSelectedDistrict] = useState<string>('부산진구');
  const [selectedRange, setSelectedRange] = useState<string>('1M');

  const [data, setData] = useState<ChartData<'line' | 'bar'> | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: '아파트 실거래가 추이',
        font: {
          size: 20,
        },
      },
    },
    scales: {
      y: {
        position: 'left',
        title: {
          display: true,
          text: '평균 거래가(만원)',
        },
        ticks: {
          callback: function (value) {
            return value.toLocaleString('ko-KR');
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        }
      },
      y1: {
        position: 'right',
        title: {
          display: true,
          text: '거래량',
        },
        grid: {
          display: false,
        },
      },
      x: {
        title: {
          display: true,
          text: getRangeTitle(selectedRange),
        },
        grid: {
          display: false
        },
        ticks: {
          maxTicksLimit: getMaxTicksLimit(selectedRange), // 기간별 최대 틱 수 설정
          autoSkip: true, // 자동으로 레이블 건너뛰기
        }
      },
    },
    interaction: {
      intersect: false,
      mode: 'index',
    },
  };

  // API에서 데이터 가져오기
  const fetchTradeData = async (district: string) => {
    try {
      setIsLoading(true);
      const endpoint = `http://localhost:8000/api/v1/apartment-trade-histories?sigungu_name=${district}&range_value=${selectedRange}`;

      const response = await fetch(endpoint);
      const response_json: ApiResponse<TradeStats[]> = await response.json();
      const tradeStats: TradeStats[] = response_json.data.stats;

      // 데이터 가공
      const processedData: ChartData<'line'> = {
        labels: tradeStats.map(stat => {
          const date = new Date(stat.tradeDate);
          return formatDate(date, selectedRange);
        }),
        datasets: [{
          label: `${selectedDistrict} 평균 거래가`,
          data: tradeStats.map(stat => stat.averagePrice),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
          tension: 0.3,
          yAxisID: 'y',
        }, {
          label: `${selectedDistrict} 거래량`,
          data: tradeStats.map(stat => stat.volume),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          tension: 0.3,
          yAxisID: 'y1',
          type: 'bar' as const,
        }]
      };

      setData(processedData);
    } catch (error) {
      console.error('데이터 가져오기 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

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
          data: data || {
            labels: [],
            datasets: [],
          },
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

  // 시군구, 기간 선택 시 차트 데이터 업데이트
  useEffect(() => {
    if (selectedDistrict && selectedRange) {
      fetchTradeData(selectedDistrict);
    }
  }, [selectedDistrict, selectedRange]);

  // 시군구 선택 핸들러
  const handleDistrictClick = (district: string) => {
    setSelectedDistrict(district);
  };

  // 기간 선택 핸들러
  const handleRangeClick = (range: string) => {
    setSelectedRange(range);
  };

  return (
    <div className="flex flex-col md:flex-row">
      {/* 사이드 네비게이션 */}
      <aside className="w-full md:w-48 bg-white rounded-lg shadow-sm p-4">
        {' '}
        {/* 너비를 48로 줄임 */}
        <h2 className="text-xl font-semibold mb-4">구 선택</h2>
        <ul className="space-y-2">
          {districtData.map((district) => (
            <li key={district}>
              <button
                className={`w-full px-4 py-2 text-left rounded-lg transition-colors
                                ${selectedDistrict === district
                    ? 'bg-blue-500 text-white'
                    : 'hover:bg-gray-100'
                  }`}
                onClick={() => handleDistrictClick(district)}
              >
                {district}
              </button>
            </li>
          ))}
        </ul>
      </aside>

      {/* 메인 컨텐츠 */}
      <div className="flex-1">
        <div className="bg-white rounded-lg shadow-sm p-6">
          {/* 기간 선택 버튼 추가 */}
          <div className="flex justify-center gap-2 mb-4">
            {['1W', '1M', '3M', '6M', '1Y', '3Y'].map((range) => (
              <button
                key={range}
                className={`px-3 py-1 rounded ${selectedRange === range
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 hover:bg-gray-200'
                  }`}
                onClick={() => handleRangeClick(range)}
              >
                {getRangeTitle(range)}
              </button>
            ))}
          </div>
          <h1 className="text-2xl font-bold text-center mb-2">
            {selectedDistrict} 아파트 실거래가 추이
          </h1>
          <p className="text-gray-600 text-center mb-8">
            최신 부동산 실거래가 데이터를 시각화하여 제공합니다.
          </p>
          {isLoading ? (
            <div className="w-full h-[500px] flex items-center justify-center">
              <div className="text-gray-500">데이터를 불러오는 중...</div>
            </div>
          ) : (
            <div className="w-full h-[500px] relative">
              <canvas ref={chartRef} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
