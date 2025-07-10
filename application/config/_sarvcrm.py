import os
from typing import Dict, Any
from sarvcrm_api import SarvURL

sarv_config: Dict[str, Any] = {
    'url': os.environ.get('SARVCRM_URL', SarvURL),
    'utype': os.environ.get('SARVCRM_UTYPE'),
    'username': os.environ.get('SARVCRM_USERNAME'),
    'password': os.environ.get('SARVCRM_PASSWORD'),
    'login_type': os.environ.get('SARVCRM_LOGIN_TYPE'),
    'language': os.environ.get('SARVCRM_LANGUAGE', 'en_US'),
    'is_password_md5': os.environ.get('SARVCRM_IS_PASSWORD_MD5', False),
}