from datetime import datetime

def ks_str_to_date(point_date):
    if not isinstance(point_date, str):
        return False
    
    point_date = point_date.split(".")[0]
    point_date = point_date.rstrip("Z")

    try:
        return datetime.strptime(point_date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return False
