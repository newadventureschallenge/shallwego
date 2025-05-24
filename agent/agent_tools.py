from dotenv import load_dotenv

from tools.calendar_tools import create_calendar, get_calendar_list, update_calendar, delete_calendar
from tools.search_tools import daum_web_search

load_dotenv()

tools = [
    daum_web_search,
    get_calendar_list, create_calendar, update_calendar, delete_calendar,
]
