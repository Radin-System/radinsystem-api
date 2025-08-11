from application import create_app
from application.config import Config
from application.jobs import JobRegistry
from application.utils import init_logging

init_logging(
    log_file = str(Config.LOG_FILE.load_value()),
    log_level = str(Config.LOG_LEVEL.load_value()),
)
app = create_app(__name__)

if __name__ == '__main__':
    JobRegistry.start_all()
    app.run(
        host = str(Config.FLASK_HOST.load_value()),
        port = int(Config.FLASK_PORT.load_value() or 8080),
        debug = bool(Config.FLASK_DEBUG.load_value())
    )
    JobRegistry.stop_all()