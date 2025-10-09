"""
Custom Jinja2 filters for the web application
"""
from utils.timezone_utils import format_jakarta_time

def jakarta_time(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """
    Convert datetime to Jakarta timezone and format it
    
    Args:
        dt: datetime object
        format_str: format string
        
    Returns:
        str: Formatted datetime string in Jakarta timezone
    """
    return format_jakarta_time(dt, format_str)

def jakarta_time_short(dt):
    """
    Convert datetime to Jakarta timezone and format it as short time (HH:MM)
    
    Args:
        dt: datetime object
        
    Returns:
        str: Formatted time string in Jakarta timezone
    """
    return format_jakarta_time(dt, '%H:%M')

def jakarta_date(dt):
    """
    Convert datetime to Jakarta timezone and format it as date (YYYY-MM-DD)
    
    Args:
        dt: datetime object
        
    Returns:
        str: Formatted date string in Jakarta timezone
    """
    return format_jakarta_time(dt, '%Y-%m-%d')


