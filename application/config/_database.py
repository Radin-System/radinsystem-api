import os
from typing import Dict, Any

database_configs: Dict[str, Any] = {
    'scheme' : os.environ.get('DATABASE_SCHEME', 'SQLITE'),
    'database': os.environ.get('DATABASE_NAME', 'radin_api'),
    'username': os.environ.get('DATABASE_USERNAME'),
    'password': os.environ.get('DATABASE_PASSWORD'),
    'host': os.environ.get('DATABASE_HOST'),
    'port': int(os.environ.get('DATABASE_PORT', 0))
}
