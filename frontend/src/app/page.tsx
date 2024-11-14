import ChartSection from './components/ChartSection';
import Carousel from './components/Carousel';
import chartData from './data/charts';
import carouselData from './data/carousel';

export default function Home() {
  return (
    <main className="p-4">
      {/* 차트 섹션 */}
      <h1 className="text-3xl font-bold mb-4 mt-4 text-gray-800">
        부산 아파트 실거래 추이
      </h1>
      <ChartSection chartData={chartData} />

      <h1 className="text-3xl font-bold mb-4 mt-12 text-gray-800">
        최근 부산 아파트 실거래
      </h1>

      {/* 캐러셀 섹션 - 카드 형식으로 변경 */}
      <section className="mt-8">
        <Carousel items={carouselData} />
      </section>
    </main>
  );
}
