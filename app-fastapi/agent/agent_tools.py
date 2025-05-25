"""
에이전트 툴 노드 정리
"""

from tools.calendar_tools import create_calendar, get_calendar_list, update_calendar, delete_calendar, get_holidays
from tools.event_tools import create_event, get_event_list, get_event_detail, update_event, delete_event
from tools.local_tools import search_places_by_keyword, search_places_by_category
from tools.search_tools import daum_web_search
from tools.task_tools import create_task, get_tasks, records_task, update_task, complete_task, delete_task


tools = [
    daum_web_search, # 웹 검색 도구
    get_calendar_list, create_calendar, update_calendar, delete_calendar, get_holidays, # 캘린더 API
    create_event, get_event_list, get_event_detail, update_event, delete_event, # 일정 API
    create_task, get_tasks, records_task, update_task, complete_task, delete_task, # 할 일 API
    search_places_by_keyword, search_places_by_category, # 장소 검색 도구
]
