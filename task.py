
import time
import logging
import sys
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


INTERVAL = 10 * 60

def createtask(yayClient, func, *args, **kwargs):
    t = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
    return t

def starttask(yayClient, task, interval=INTERVAL):
    next_run = time.time()
    try:
        while True:
            now = time.time()
            if now < next_run:
                time.sleep(next_run - now)
            try:
                createtask(yayClient, task).start()
            except Exception:
                logging.exception("task failed")
            next_run += interval
    except KeyboardInterrupt:
        logging.info("stopped by user")
        sys.exit(0)