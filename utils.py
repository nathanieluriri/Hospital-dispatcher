from datetime import datetime, timedelta

def is_30_minutes_apart(given_time_str: str) -> bool:
    if given_time_str:
        # Parse the string to a datetime object
        given_time = datetime.fromisoformat(given_time_str)
        now = datetime.now()

        # Calculate the time difference
        difference = abs(now - given_time)

        # Check if the difference is at least 30 minutes
        return difference >= timedelta(minutes=30)
    return False