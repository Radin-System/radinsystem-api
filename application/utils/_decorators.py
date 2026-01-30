import ipaddress
from functools import wraps
from flask import abort


def private_addresses_only(request, config=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not config:
                return func(*args, **kwargs)

            try:
                ip = ipaddress.ip_address(
                    request.headers.get('X-Real-IP', request.remote_addr)
                )
                abort(403) if not ip.is_private else None

            except ValueError:
                abort(403)

            return func(*args, **kwargs)
        return wrapper
    return decorator
