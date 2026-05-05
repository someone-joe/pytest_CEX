"""
Utility Functions
"""
import logging
import time
from datetime import datetime


def setup_logging(level="INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def get_timestamp():
    """Get current timestamp in milliseconds"""
    return int(time.time() * 1000)


def format_timestamp(ms_timestamp):
    """Format millisecond timestamp to readable string"""
    return datetime.fromtimestamp(ms_timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")


def validate_response(response, required_keys=None):
    """Validate API response"""
    if "error" in response:
        return False, response.get("error")

    if required_keys:
        for key in required_keys:
            if key not in response:
                return False, f"Missing required key: {key}"

    return True, "Success"


class RetryDecorator:
    """Retry decorator for flaky API calls"""

    def __init__(self, max_attempts=3, delay=1):
        self.max_attempts = max_attempts
        self.delay = delay

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self.max_attempts - 1:
                        raise
                    time.sleep(self.delay)
        return wrapper
