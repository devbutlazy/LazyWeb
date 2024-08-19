from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import List, Dict


class CustomRateLimiter:
    def __init__(self, limit: int, period: timedelta):
        """
        Initialize the rate limiter with a limit and time period.

        :param limit: The maximum number of allowed requests within the period.
        :param period: The time period during which requests are counted.
        """
        self.limit = limit
        self.period = period
        self.requests: Dict[str, List[datetime]] = defaultdict(list)

    async def is_allowed(self, key: str) -> bool:
        """
        Check if a request is allowed based on the rate limit.

        :param key: Identifier for the requestor (e.g., IP address or user ID).
        :return: True if the request is allowed, False otherwise.
        """
        now = datetime.now(timezone.utc)
        period_start = now - self.period
        self._cleanup_requests(key, period_start)

        if len(self.requests[key]) < self.limit:
            self.requests[key].append(now)
            return True
        
        return False

    def _cleanup_requests(self, key: str, period_start: datetime) -> None:
        """
        Remove requests that are outside the current time period.

        :param key: Identifier for the requestor.
        :param period_start: The start time of the period to keep.
        """
        self.requests[key] = [
            timestamp for timestamp in self.requests[key] if timestamp > period_start
        ]
