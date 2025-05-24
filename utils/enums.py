from enum import Enum


class ColorEnum(str, Enum):
    """톡캘린더 색상 옵션"""
    BLUE = "BLUE"
    ROYAL_BLUE = "ROYAL_BLUE"
    NAVY_BLUE = "NAVY_BLUE"
    RED = "RED"
    PINK = "PINK"
    ORANGE = "ORANGE"
    GREEN = "GREEN"
    LIME = "LIME"
    OLIVE = "OLIVE"
    MINT = "MINT"
    MAGENTA = "MAGENTA"
    VIOLET = "VIOLET"
    LAVENDER = "LAVENDER"
    BROWN = "BROWN"
    GRAY = "GRAY"


class CategoryGroupCode(str, Enum):
    """
    카카오 로컬 검색 카테고리 그룹 코드
    """
    MT1 = "MT1"
    CS2 = "CS2"
    PS3 = "PS3"
    SC4 = "SC4"
    AC5 = "AC5"
    PK6 = "PK6"
    OL7 = "OL7"
    SW8 = "SW8"
    BK9 = "BK9"
    CT1 = "CT1"
    AG2 = "AG2"
    PO3 = "PO3"
    AT4 = "AT4"
    AD5 = "AD5"
    FD6 = "FD6"
    CE7 = "CE7"
    HP8 = "HP8"
    PM9 = "PM9"

    class Config:
        """
        Pydantic 설정
        """
        json_schema_extra = {
            "description": "카카오 로컬 검색 카테고리 그룹 코드",
            "x-enumDescription": {
                "MT1": "대형마트",
                "CS2": "편의점",
                "PS3": "어린이집, 유치원",
                "SC4": "학교",
                "AC5": "학원",
                "PK6": "주차장",
                "OL7": "주유소, 충전소",
                "SW8": "지하철역",
                "BK9": "은행",
                "CT1": "문화시설",
                "AG2": "중개업소",
                "PO3": "공공기관",
                "AT4": "관광명소",
                "AD5": "숙박",
                "FD6": "음식점",
                "CE7": "카페",
                "HP8": "병원",
                "PM9": "약국"
            }
        }
