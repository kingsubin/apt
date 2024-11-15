from datetime import date
from pydantic import Field, computed_field
from src.schemas.pydantic_base import PydanticBaseModel


class ApartmentTradeHistoryModel(PydanticBaseModel):
    id: int
    법정동시군구코드: str
    법정동읍면동코드: str
    법정동지번코드: str | None
    법정동본번코드: str | None
    법정동부번코드: str | None
    도로명: str | None
    도로명시군구코드: str | None
    도로명코드: str | None
    도로명일련번호코드: str | None
    도로명지상지하코드: str | None
    도로명건물본번호코드: str | None
    도로명건물부번호코드: str | None
    법정동: str
    단지명: str
    지번: str | None
    전용면적: float | None
    계약년도: str
    계약월: str
    계약일: str
    거래금액: int
    층: int | None
    건축년도: str | None
    해제여부: str | None
    해제사유발생일: date | None
    거래유형: str | None
    중개사소재지: str | None
    등기일자: date | None
    아파트동명: str | None
    매도자: str | None
    매수자: str | None
    토지임대부아파트여부: str | None

    @computed_field
    def trade_date(self) -> date:
        return date(int(self.계약년도), int(self.계약월), int(self.계약일))


class ApartmentTradeHistoryOutput(ApartmentTradeHistoryModel):
    법정동지번코드: str | None = Field(exclude=True)
    법정동본번코드: str | None = Field(exclude=True)
    법정동부번코드: str | None = Field(exclude=True)
    도로명시군구코드: str | None = Field(exclude=True)
    도로명코드: str | None = Field(exclude=True)
    도로명일련번호코드: str | None = Field(exclude=True)
    도로명지상지하코드: str | None = Field(exclude=True)
    중개사소재지: str | None = Field(exclude=True)
    등기일자: date | None = Field(exclude=True)
    아파트동명: str | None = Field(exclude=True)
    매도자: str | None = Field(exclude=True)
    매수자: str | None = Field(exclude=True)
    토지임대부아파트여부: str | None = Field(exclude=True)
