import ipaddress
from typing import Any
from functools import wraps
from flask import request, abort

def token_required(client) -> Any:
    if 'Authorization' in request.headers:
        _, token = request.headers.get('Authorization', ' ').split('Token ', 1)
        tenant = client.tenancy

def private_addresses_only(_func=None, *, config=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not config:
                return func(*args, **kwargs)

            try:
                ip = ipaddress.ip_address(request.remote_addr or '')
                abort(403) if not ip.is_private else None

            except ValueError:
                abort(403)

            return func(*args, **kwargs)
        return wrapper

    # Allow decorator to be used with or without arguments
    if _func is None:
        return decorator
    else:
        return decorator(_func)