from datetime import date, timedelta
from enum import StrEnum

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Environment(StrEnum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)


class RangeValue(StrEnum):
    ONE_WEEK = "1W"
    ONE_MONTH = "1M"
    THREE_MONTH = "3M"
    SIX_MONTH = "6M"
    ONE_YEAR = "1Y"
    MAX = "MAX"

    @classmethod
    def to_start_date(cls, range_value: "RangeValue") -> date:
        year, month, day = cls.to_start_year_month_day(range_value)
        return date(year, month, day)

    @classmethod
    def to_start_year_month_day(cls, range_value: "RangeValue") -> tuple[int, int, int]:
        today = date.today()

        if range_value == cls.ONE_WEEK:
            one_week_ago = today - timedelta(weeks=1)
            return one_week_ago.year, one_week_ago.month, one_week_ago.day
        elif range_value == cls.ONE_MONTH:
            one_month_ago = today - timedelta(weeks=4)
            return one_month_ago.year, one_month_ago.month, one_month_ago.day
        elif range_value == cls.THREE_MONTH:
            three_month_ago = today - timedelta(weeks=12)
            return three_month_ago.year, three_month_ago.month, three_month_ago.day
        elif range_value == cls.SIX_MONTH:
            six_month_ago = today - timedelta(weeks=24)
            return six_month_ago.year, six_month_ago.month, six_month_ago.day
        elif range_value == cls.ONE_YEAR:
            one_year_ago = today - timedelta(weeks=52)
            return one_year_ago.year, one_year_ago.month, one_year_ago.day
        elif range_value == cls.MAX:
            return 2010, 1, 1


class SigunguName(StrEnum):
    중구 = "중구"
    서구 = "서구"
    동구 = "동구"
    영도구 = "영도구"
    부산진구 = "부산진구"
    동래구 = "동래구"
    남구 = "남구"
    북구 = "북구"
    해운대구 = "해운대구"
    사하구 = "사하구"
    금정구 = "금정구"
    강서구 = "강서구"
    연제구 = "연제구"
    수영구 = "수영구"
    사상구 = "사상구"
    기장군 = "기장군"

    @classmethod
    def to_code(cls, sigungu_name: str) -> str:
        sigungu_codes = {
            cls.중구: "26110",
            cls.서구: "26140",
            cls.동구: "26170",
            cls.영도구: "26200",
            cls.부산진구: "26230",
            cls.동래구: "26260",
            cls.남구: "26290",
            cls.북구: "26320",
            cls.해운대구: "26350",
            cls.사하구: "26380",
            cls.금정구: "26410",
            cls.강서구: "26440",
            cls.연제구: "26470",
            cls.수영구: "26500",
            cls.사상구: "26530",
            cls.기장군: "26710",
        }
        return sigungu_codes.get(sigungu_name)
