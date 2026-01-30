from application import create_app
from application.config import app_config
from application.utils import init_logging

init_logging(
    log_file = str(app_config.log_file),
    log_level = app_config.log_level,
)
app = create_app(__name__)

if __name__ == '__main__':
    import active_jobs as _
    from application.jobs import JobRegistry
    JobRegistry.start_all()
    app.run(
        host = app_config.flask_host,
        port = app_config.flask_port,
        debug = app_config.flask_debug,
    )
    JobRegistry.stop_all()