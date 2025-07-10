# Load Dotenv first
try:
    import dotenv
    dotenv.load_dotenv()
except ImportError: pass

from flask import Flask
from application.__version__ import __version__
from application.utils import init_logging
from application.config import logging_config, flask_configs, flask_run_configs
from application.blueprints import blueprints

init_logging(**logging_config)

app = Flask(__name__)
app.config.update(flask_configs)
[app.register_blueprint(blueprint) for blueprint in blueprints]


if __name__ == '__main__':
    app.run(**flask_run_configs)