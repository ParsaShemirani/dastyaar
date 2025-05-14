from enum import Enum
from datetime import datetime
from typing import Tuple


class Precision(Enum):
    YEAR   = 'year'
    MONTH  = 'month'
    DAY    = 'day'
    HOUR   = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'


def make_ts(year: int, month: int = None, day: int = None, 
           hour: int = None, minute: int = None, second: int = None) -> Tuple[str, str]:
    """Build a datetime and precision based on which components are set.
    
    Returns:
        Tuple[str, str]: A tuple containing (timestamp_string, precision_value)
    """
    if second is not None:
        prec = Precision.SECOND
    elif minute is not None:
        prec = Precision.MINUTE
    elif hour is not None:
        prec = Precision.HOUR
    elif day is not None:
        prec = Precision.DAY
    elif month is not None:
        prec = Precision.MONTH
    else:
        prec = Precision.YEAR

    # fill defaults
    month  = month  or 1
    day    = day    or 1
    hour   = hour   or 0
    minute = minute or 0
    second = second or 0

    dt = datetime(year, month, day, hour, minute, second)
    ts = dt.strftime("%Y-%m-%d %H:%M:%S")
    return ts, prec.value


def new_ts() -> Tuple[str, str]:
    """Interactively collect timestamp components and return formatted timestamp with precision.
    
    Returns:
        Tuple[str, str]: A tuple containing (timestamp_string, precision_value)
    """
    try:
        year = input("Enter year (YYYY): ")
        if not year:
            return None
        year = int(year)
        
        month = input("Enter month (1-12, or press Enter to skip): ")
        if not month:
            return make_ts(year)
        month = int(month)
        
        day = input("Enter day (1-31, or press Enter to skip): ")
        if not day:
            return make_ts(year, month)
        day = int(day)
        
        hour = input("Enter hour (0-23, or press Enter to skip): ")
        if not hour:
            return make_ts(year, month, day)
        hour = int(hour)
        
        minute = input("Enter minute (0-59, or press Enter to skip): ")
        if not minute:
            return make_ts(year, month, day, hour)
        minute = int(minute)
        
        second = input("Enter second (0-59, or press Enter to skip): ")
        if not second:
            return make_ts(year, month, day, hour, minute)
        second = int(second)
        
        return make_ts(year, month, day, hour, minute, second)
        
    except ValueError as e:
        print(f"Error: Please enter valid numbers: {e}")
        return None
