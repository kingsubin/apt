from datetime import datetime, date
from zoneinfo import ZoneInfo

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict


def datetime_to_gmt_str(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: datetime_to_gmt_str},
        populate_by_name=True,
    )

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)

class ApartmentTradeHistory(CustomModel):
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
    매수자: str
    토지임대부아파트여부: str | None
