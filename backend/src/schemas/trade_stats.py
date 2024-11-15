from datetime import date
from src.schemas.pydantic_base import PydanticBaseModel
from pydantic import computed_field


class TradeStats(PydanticBaseModel):
    trade_date: date
    volume: int = 0
    total_price: int = 0

    @computed_field
    def average_price(self) -> int:
        return int(self.total_price / self.volume) if self.volume else 0
