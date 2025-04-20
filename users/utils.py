from datetime import timedelta

def get_week_range(date):
    """Given any date, return the Sunday–Saturday week range."""
    start = date - timedelta(days=date.weekday() + 1 if date.weekday() != 6 else 0)
    end = start + timedelta(days=6)
    return start, end

def get_day_display(day_code):
    """Translate short day code (e.g. 'mon') to full weekday name."""
    day_map = {
        'sun': 'Sunday', 'mon': 'Monday', 'tue': 'Tuesday',
        'wed': 'Wednesday', 'thu': 'Thursday', 'fri': 'Friday', 'sat': 'Saturday'
    }
    return day_map.get(day_code.lower(), day_code)
