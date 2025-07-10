from typing import Any
from functools import wraps
from flask import request

from api_connections import netbox_connection


def token_required() -> Any:
    if 'Authorization' in request.headers:
        _, token = request.headers.get('Authorization', ' ').split('Bearer ', 1)
        tenant = netbox_connection.tenancy
