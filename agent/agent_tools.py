from dotenv import load_dotenv

from tools.calendar_tools import create_calendar, get_calendar_list, update_calendar, delete_calendar
from tools.event_tools import create_event, get_event_list, get_event_detail, update_event, delete_event
from tools.search_tools import daum_web_search

load_dotenv()

tools = [
    daum_web_search,
    get_calendar_list, create_calendar, update_calendar, delete_calendar,
    create_event, get_event_list, get_event_detail, update_event, delete_event
]
