from dotenv import load_dotenv

from tools.calendar_tools import create_calendar, get_calendar_list, update_calendar, delete_calendar, get_holidays
from tools.event_tools import create_event, get_event_list, get_event_detail, update_event, delete_event
from tools.local_tools import search_places_by_keyword, search_places_by_category
from tools.search_tools import daum_web_search
from tools.task_tools import create_task, get_tasks, records_task, update_task, complete_task, delete_task

load_dotenv()

tools = [
    daum_web_search,
    get_calendar_list, create_calendar, update_calendar, delete_calendar, get_holidays,
    create_event, get_event_list, get_event_detail, update_event, delete_event,
    create_task, get_tasks, records_task, update_task, complete_task, delete_task,
    search_places_by_keyword, search_places_by_category,
]
