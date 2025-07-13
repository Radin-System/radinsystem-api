import os
from typing import Dict, Any

ami_configs: Dict[str, Any] = {
    'host': os.environ.get('AMI_HOST'),
    'port': int(os.environ.get('AMI_PORT', 5038)),
    'Username': os.environ.get('AMI_USERNAME'),
    'Secret': os.environ.get('AMI_SECRET'),
    'AuthType': os.environ.get('AMI_AUTHTYPE'),
    'Key': os.environ.get('AMI_KEY'),
    'Events': os.environ.get('AMI_EVENTS'),
}