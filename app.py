from application import create_app
from application.config import logging_config, flask_run_configs
from application.utils import init_logging

init_logging(**logging_config)
app = create_app(__name__)

if __name__ == '__main__':
    app.run(**flask_run_configs)