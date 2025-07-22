from .agent import agent_bp
from .callcenter import callcenter_bp
from .dev import dev_bp
from .diagnose import diagnose_bp
from .root import root_bp


all_blueprints = [
    agent_bp,
    callcenter_bp,
    dev_bp,
    diagnose_bp,
    root_bp,
]


__all__ = [
    'all_blueprints',
    'agent_bp',
    'callcenter_bp',
    'dev_bp',
    'diagnose_bp',
    'root_bp',
]