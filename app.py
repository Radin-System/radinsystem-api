# Load Dotenv first
try:
    import dotenv # type: ignore
    dotenv.load_dotenv()
except ImportError: pass

from flask import Flask

from __version__ import __version__
from utils import initiate_logging
from config import logging_config, flask_configs, flask_run_configs
from blueprints import blueprints

initiate_logging(logging_config)

app = Flask(__name__)
app.config.update(flask_configs)
[app.register_blueprint(blueprint) for blueprint in blueprints]


if __name__ == '__main__':
    app.run(**flask_run_configs)