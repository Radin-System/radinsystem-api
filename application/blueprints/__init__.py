from .callcenter import callcenter_bp
from .diagnose import diagnose_bp
from .root import root_bp

blueprints = [
    callcenter_bp,
    diagnose_bp,
    root_bp,
]

__all__ = [
    'callcenter_bp',
    'diagnose_bp',
    'root_bp',
]