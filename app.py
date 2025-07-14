import sys
from application.config import logging_config, flask_run_configs
from application.utils import init_logging
from application import create_app

init_logging(**logging_config)
app = create_app(__name__)
app.run(**flask_run_configs)