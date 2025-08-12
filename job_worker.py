import sys, time, signal, logging
from application.jobs import JobRegistry
from application.config import Config
from application.utils import init_logging

running = True

init_logging(
    log_file = str(Config.LOG_FILE.load_value()),
    log_level = str(Config.LOG_LEVEL.load_value()),
)

logger = logging.getLogger()

def handle_signal(signum, frame):
    global running, logger
    logger.info(f"Received signal {signum}, shutting down...")
    running = False


if __name__ == '__main__':
    import active_jobs as _  # init jobs

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    JobRegistry.start_all()

    try:
        while running:
            time.sleep(1)

    finally:
        JobRegistry.stop_all()
        logger.info("Jobs stopped. Exiting...")
        sys.exit(0)
