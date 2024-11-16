'use client';

import React, { useEffect, useRef } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  Title,
  Tooltip,
} from 'chart.js';
import { Chart } from 'chart.js';
import ChartItem from '@/types/chart-item';

ChartJS.register(
  LineController,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip
);

const ChartDisplay: React.FC<ChartItem> = ({ title, value, change, data }) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    if (chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      if (ctx) {
        // 이전 차트 인스턴스 제거
        if (chartInstance.current) {
          chartInstance.current.destroy();
        }

        // 새로운 차트 생성
        chartInstance.current = new Chart(ctx, {
          type: 'line',
          data: {
            labels: new Array(data.length).fill(''), // 라벨 숨기기
            datasets: [
              {
                data: data,
                borderColor:
                  change >= 0 ? 'rgb(239, 68, 68)' : 'rgb(59, 130, 246)',
                borderWidth: 1.5,
                tension: 0.4,
                pointRadius: 0,
                fill: false,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false,
              },
              tooltip: {
                enabled: false,
              },
            },
            scales: {
              x: {
                display: false,
              },
              y: {
                display: false,
              },
            },
            elements: {
              line: {
                tension: 0.4,
              },
            },
          },
        });
      }
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
    // }, [data]);
  });

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-semibold">{title}</h3>
      <div className="flex items-baseline mt-2">
        <span className="text-2xl font-bold">{value.toLocaleString()}</span>
        <span
          className={`ml-2 ${change >= 0 ? 'text-red-500' : 'text-blue-500'}`}
        >
          {change >= 0 ? '+' : ''}
          {change}%
        </span>
      </div>
      {/* 차트 캔버스 추가 */}
      <div className="h-[100px] mt-4">
        <canvas ref={chartRef}></canvas>
      </div>
    </div>
  );
};

ChartDisplay.displayName = 'ChartDisplay';

export default ChartDisplay;
