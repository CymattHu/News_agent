import logging
from time import sleep
from functools import wraps

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")
log = logging.getLogger("news-agent")

def retry(times=3, delay=1):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    log.warning(f"{func.__name__} failed (attempt {i+1}/{times}): {e}")
                    sleep(delay)
            raise last_exc
        return wrapper
    return deco
