import datetime
import time

def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M:%S')

def parse_datetime_str(datetime_str):
    try:
        dt = datetime.datetime.strptime(datetime_str, '%d.%m.%Y %H:%M:%S')
        return time.mktime(dt.timetuple())
    except ValueError:
        return None

def fix_keyboard_bindings(window):
    window.bind_all("<Control-v>", lambda e: window.focus_get().event_generate("<<Paste>>"))
    window.bind_all("<Control-c>", lambda e: window.focus_get().event_generate("<<Copy>>"))
    window.bind_all("<Control-a>", lambda e: window.focus_get().event_generate("<<SelectAll>>"))