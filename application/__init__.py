import os
from typing import Dict
from .utils import calculate_file_sha256, create_agent_file_path, AGENT_FOLDER

agent_packages: Dict[str, str] = {}


def load_agent_packages():
    global agent_packages
    agent_packages = {}
    for version in os.listdir(AGENT_FOLDER):
        exe_path = create_agent_file_path(version)
        if os.path.exists(exe_path):
            agent_packages[version] = calculate_file_sha256(exe_path)

def create_app(name: str):
    from flask import Flask
    from .config import Config
    from .blueprints import all_blueprints

    app = Flask(name)
    app.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
    [app.register_blueprint(blueprint) for blueprint in all_blueprints]

    return app

load_agent_packages()

__all__ = [
    'create_app',
]