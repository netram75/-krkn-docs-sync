import logging
import time

logger = logging.getLogger(__name__)


def retry(func, attempts=3, delay=1.0):
    for i in range(attempts):
        try:
            return func()
        except Exception as exc:
            if i == attempts - 1:
                raise
            logger.warning("attempt %d failed: %s", i + 1, exc)
            time.sleep(delay)


def parse_duration(value: str) -> float:
    units = {"s": 1, "m": 60, "h": 3600}
    return float(value[:-1]) * units.get(value[-1], 1)
