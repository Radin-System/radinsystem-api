import os
from typing import Dict, Any

callcenter_configs: Dict[str, Any] = {
    'phonebook_password': os.environ.get('PHONEBOOK_PASSWORD', None),
    'phonebook_password_required': os.environ.get('PHONEBOOK_PASSWORD_REQUIRED', False),
    'phonebook_local_only': os.environ.get('PHONEBOOK_LOCAL_ONLY', False),
}
