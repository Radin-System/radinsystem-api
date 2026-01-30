from .callcenter import callcenter_bp
from .diagnose import diagnose_bp
from .root import root_bp


all_blueprints = [
    callcenter_bp,
    diagnose_bp,
    root_bp,
]


__all__ = [
    'all_blueprints',
    'callcenter_bp',
    'diagnose_bp',
    'root_bp',
]