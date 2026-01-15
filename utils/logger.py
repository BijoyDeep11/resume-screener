import time
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_time(start, label="Process"):
    duration = round(time.time() - start, 2)
    logging.info(f"{label} took {duration}s")
    return duration
