from datetime import date, timedelta
from sqlalchemy import Select, select
from src.schemas.apartment_trade_history import ApartmentTradeHistoryModel
from src.schemas.trade_stats import TradeStats
from src.core.constants import RangeValue
from src.api.dependencies import TradeHistoryFilter
from src.db.database import fetch_all
from src.db.models.apartment_trade_history import ApartmentTradeHistory


class ApartmentTradeHistoryService:
    async def get_trade_stats(
        self, trade_filter: TradeHistoryFilter
    ) -> list[TradeStats]:
        trades = await self.fetch_trade_histories(trade_filter)
        date_range = self._generate_date_range(trade_filter.range_value)
        return self._calculate_trade_stats(trades, date_range)

    async def fetch_trade_histories(
        self,
        trade_filter: TradeHistoryFilter,
    ) -> list[ApartmentTradeHistoryModel]:
        """거래 이력 조회"""
        query = self._build_trade_query(trade_filter)
        rows = await fetch_all(query)
        return [ApartmentTradeHistoryModel.model_validate(row) for row in rows]

    def _build_trade_query(self, trade_filter: TradeHistoryFilter) -> Select:
        """쿼리 생성"""
        query = select(ApartmentTradeHistory)

        if trade_filter.sigungu_code:
            query = query.where(
                ApartmentTradeHistory.법정동시군구코드 == trade_filter.sigungu_code
            )

        if trade_filter.range_value:
            year, month, day = RangeValue.to_start_year_month_day(
                trade_filter.range_value
            )
            query = query.where(
                ApartmentTradeHistory.계약년도 >= year,
                ApartmentTradeHistory.계약월 >= month,
                ApartmentTradeHistory.계약일 >= day,
            )

        return query

    def _generate_date_range(self, range_value: str) -> list[date]:
        """날짜 범위 생성"""
        start_date = RangeValue.to_start_date(range_value)
        today = date.today()
        return [
            start_date + timedelta(days=x) for x in range((today - start_date).days + 1)
        ]

    def _calculate_trade_stats(
        self, trades: list[ApartmentTradeHistoryModel], dates: list[date]
    ) -> list[TradeStats]:
        """거래 통계 계산"""
        stats_by_date: dict[date, TradeStats] = {
            date_: TradeStats(trade_date=date_) for date_ in dates
        }

        for trade in trades:
            if trade.trade_date in stats_by_date:
                stats = stats_by_date[trade.trade_date]
                stats.volume += 1
                stats.total_price += trade.거래금액

        return list(stats_by_date.values())


apartment_trade_history_service = ApartmentTradeHistoryService()
