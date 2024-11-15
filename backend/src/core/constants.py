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
