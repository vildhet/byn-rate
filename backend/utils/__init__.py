from datetime import timezone

def utc_timestamp(dt):
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())