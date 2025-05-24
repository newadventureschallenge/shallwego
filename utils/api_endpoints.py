"""
카카오 API 엔드포인트 정의
"""

KAKAO_API_OAUTH = "https://kauth.kakao.com/oauth/authorize"
KAKAO_API_TOKEN = "https://kauth.kakao.com/oauth/token"
KAKAO_API_USER = "https://kapi.kakao.com/v2/user/me"

KAKAO_DAUM_SEARCH_URL = "https://dapi.kakao.com/v2/search/web"

KAKAO_CALENDAR_BASE_URL = "https://kapi.kakao.com/v2/api/calendar"

KAKAO_GET_CALENDAR_URL = f"{KAKAO_CALENDAR_BASE_URL}/calendars"
KAKAO_CREATE_CALENDAR_URL = f"{KAKAO_CALENDAR_BASE_URL}/create/calendar"
KAKAO_UPDATE_CALENDAR_URL = f"{KAKAO_CALENDAR_BASE_URL}/update/calendar"
KAKAO_DELETE_CALENDAR_URL = f"{KAKAO_CALENDAR_BASE_URL}/delete/calendar"

KAKAO_CREATE_EVENT_URL = f"{KAKAO_CALENDAR_BASE_URL}/create/event"
KAKAO_GET_EVENTS_URL = f"{KAKAO_CALENDAR_BASE_URL}/events"
KAKAO_GET_EVENT_URL = f"{KAKAO_CALENDAR_BASE_URL}/event"
KAKAO_UPDATE_EVENT_URL = f"{KAKAO_CALENDAR_BASE_URL}/update/event/host"
KAKAO_DELETE_EVENT_URL = f"{KAKAO_CALENDAR_BASE_URL}/delete/event"

API_TIMEOUT = 10
