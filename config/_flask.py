import os
from typing import Dict, Any

from utils import create_database_uri
from ._database import database_configs

flask_run_configs: Dict[str, Any] = {
    'host': os.environ.get('FLASK_HOST', '127.0.0.1'),
    'port': int(os.environ.get('FLASK_PORT', 8080)),
    'debug': os.environ.get('FLASK_DEBUG', 'true')
}

flask_configs: Dict[str, Any] = {
    'SECRET_KEY': os.environ.get('FLASK_SECRET'),
    'SQLALCHEMY_DATABASE_URI': create_database_uri(**database_configs),
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
}