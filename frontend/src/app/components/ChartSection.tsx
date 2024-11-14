import { memo } from 'react';
import ChartItem from './ChartItem';

interface ChartSectionProps {
  chartData: {
    title: string;
    value: number;
    change: number;
    data: number[];
  }[];
}

const ChartSection = memo(({ chartData }: ChartSectionProps) => {
  return (
    <section className="mt-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {chartData.map((item, index) => (
          <ChartItem
            key={index}
            title={item.title}
            value={item.value}
            change={item.change}
            data={item.data}
          />
        ))}
      </div>
    </section>
  );
});

ChartSection.displayName = 'ChartSection';

export default ChartSection;
