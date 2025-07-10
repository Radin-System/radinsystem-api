import os
from typing import Dict, Any

netbox_configs: Dict[str, Any] = {
    'url': os.environ.get('NETBOX_URL'),
    'token': os.environ.get('NETBOX_TOKEN'),
}