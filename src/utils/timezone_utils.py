"""
Timezone utilities for Jakarta (UTC+7) timezone
"""
from datetime import datetime, timezone, timedelta
import pytz

# Jakarta timezone (UTC+7)
JAKARTA_TZ = pytz.timezone('Asia/Jakarta')

def jakarta_now():
    """
    Get current datetime in Jakarta timezone (UTC+7)
    
    Returns:
        datetime: Current datetime in Jakarta timezone
    """
    return datetime.now(JAKARTA_TZ)

def utc_to_jakarta(utc_dt):
    """
    Convert UTC datetime to Jakarta timezone
    
    Args:
        utc_dt: UTC datetime object
        
    Returns:
        datetime: Jakarta timezone datetime
    """
    if utc_dt is None:
        return None
    
    if utc_dt.tzinfo is None:
        # Assume it's UTC if no timezone info
        utc_dt = pytz.utc.localize(utc_dt)
    
    return utc_dt.astimezone(JAKARTA_TZ)

def jakarta_to_utc(jakarta_dt):
    """
    Convert Jakarta datetime to UTC
    
    Args:
        jakarta_dt: Jakarta timezone datetime object
        
    Returns:
        datetime: UTC datetime
    """
    if jakarta_dt is None:
        return None
    
    if jakarta_dt.tzinfo is None:
        # Assume it's Jakarta time if no timezone info
        jakarta_dt = JAKARTA_TZ.localize(jakarta_dt)
    
    return jakarta_dt.astimezone(pytz.utc)

def format_jakarta_time(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """
    Format datetime to Jakarta timezone string
    
    Args:
        dt: datetime object
        format_str: format string
        
    Returns:
        str: Formatted datetime string in Jakarta timezone
    """
    if dt is None:
        return None
    
    if dt.tzinfo is None:
        # Assume it's UTC if no timezone info
        dt = pytz.utc.localize(dt)
    
    jakarta_dt = dt.astimezone(JAKARTA_TZ)
    return jakarta_dt.strftime(format_str)


