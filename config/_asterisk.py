import os
from typing import Dict, Any

ami_configs: Dict[str, Any] = {
    'host': os.environ.get('AMI_HOST'),
    'port': int(os.environ.get('AMI_PORT', 5038)),
    'username': os.environ.get('AMI_USERNAME'),
    'secret': os.environ.get('AMI_SECRET'),
    'auth_type': os.environ.get('AMI_AUTHTYPE'),
    'key': os.environ.get('AMI_KEY'),
    'events': os.environ.get('AMI_EVENTS'),
}