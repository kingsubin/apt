from datetime import date
from pydantic import computed_field

from src.schemas.response import CamelCaseModel


class TradeStats(CamelCaseModel):
    trade_date: date
    volume: int = 0
    total_price: int = 0

    @computed_field
    def average_price(self) -> int:
        return int(self.total_price / self.volume) if self.volume else 0
