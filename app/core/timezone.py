import os
from datetime import datetime
from zoneinfo import ZoneInfo

APP_TIMEZONE_NAME = os.environ.get("APP_TIMEZONE", "Asia/Kolkata")

APP_TIMEZONE = ZoneInfo(APP_TIMEZONE_NAME)

def get_current_localized_time():
    return datetime.now(APP_TIMEZONE)
