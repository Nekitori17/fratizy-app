from datetime import datetime
import pytz

def get_timestamp(locate_timezone):
  if locate_timezone:
    try:
      timezone = pytz.timezone(locate_timezone)
      now = datetime.now(timezone)
      return now.strftime("%a, %Y/%m/%d × %H:%M:%S. UTC%Z")
    except Exception as e:
      return str(e)
  else:
    return datetime.now().strftime("%a, %Y/%m/%d × %H:%M:%S. UTC%Z")