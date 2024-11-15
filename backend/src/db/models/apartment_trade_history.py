from sqlalchemy import BIGINT, CHAR, DECIMAL, INT, VARCHAR, DATE, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

from src.db.models.base import SQLAlchemyModel


class ApartmentTradeHistory(SQLAlchemyModel):
    __tablename__ = "apartment_trade_history"
    __table_args__ = (PrimaryKeyConstraint("id"),)

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    법정동시군구코드: Mapped[str] = mapped_column(CHAR(5))
    법정동읍면동코드: Mapped[str] = mapped_column(CHAR(5))
    법정동지번코드: Mapped[str] = mapped_column(VARCHAR(1), nullable=True)
    법정동본번코드: Mapped[str] = mapped_column(VARCHAR(4), nullable=True)
    법정동부번코드: Mapped[str] = mapped_column(VARCHAR(4), nullable=True)
    도로명: Mapped[str] = mapped_column(VARCHAR(200), nullable=True)
    도로명시군구코드: Mapped[str] = mapped_column(VARCHAR(5), nullable=True)
    도로명코드: Mapped[str] = mapped_column(VARCHAR(7), nullable=True)
    도로명일련번호코드: Mapped[str] = mapped_column(VARCHAR(2), nullable=True)
    도로명지상지하코드: Mapped[str] = mapped_column(VARCHAR(1), nullable=True)
    도로명건물본번호코드: Mapped[str] = mapped_column(VARCHAR(5), nullable=True)
    도로명건물부번호코드: Mapped[str] = mapped_column(VARCHAR(5), nullable=True)
    법정동: Mapped[str] = mapped_column(VARCHAR(120))
    단지명: Mapped[str] = mapped_column(VARCHAR(200))
    지번: Mapped[str] = mapped_column(VARCHAR(20), nullable=True)
    전용면적: Mapped[float] = mapped_column(DECIMAL(10, 4), nullable=True)
    계약년도: Mapped[str] = mapped_column(CHAR(4))
    계약월: Mapped[str] = mapped_column(CHAR(2))
    계약일: Mapped[str] = mapped_column(CHAR(2))
    거래금액: Mapped[int] = mapped_column(BIGINT)
    층: Mapped[int] = mapped_column(INT, nullable=True)
    건축년도: Mapped[str] = mapped_column(CHAR(4), nullable=True)
    단지일련번호: Mapped[str] = mapped_column(VARCHAR(20))
    해제여부: Mapped[str] = mapped_column(CHAR(1), nullable=True)
    해제사유발생일: Mapped[date] = mapped_column(DATE, nullable=True)
    거래유형: Mapped[str] = mapped_column(VARCHAR(20), nullable=True)
    중개사소재지: Mapped[str] = mapped_column(VARCHAR(300), nullable=True)
    등기일자: Mapped[date] = mapped_column(DATE, nullable=True)
    아파트동명: Mapped[str] = mapped_column(VARCHAR(400), nullable=True)
    매도자: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    매수자: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    토지임대부아파트여부: Mapped[str] = mapped_column(VARCHAR(1), nullable=True)
