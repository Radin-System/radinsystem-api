from classmods import ENVMod
from typing import Dict, Any

flask_host = ENVMod.add(
    name = 'host',
    section_name = 'flask',
    type_hint = str,
    default = '127.0.0.1',
)
flask_port = ENVMod.add(
    name = 'port',
    section_name = 'flask',
    type_hint = int,
    default = '8080',
)
flask_debug = ENVMod.add(
    name = 'debug',
    section_name = 'flask',
    type_hint = bool,
    default = 'True',
)
flask_secret_key = ENVMod.add(
    name = 'secret_key',
    section_name = 'flask',
    type_hint = str,
    required = True,
)

flask_run_configs: Dict[str, Any] = {
    'host': flask_host.load_value(),
    'port': flask_port.load_value(),
    'debug': flask_debug.load_value(),
}

flask_configs: Dict[str, Any] = {
    'SECRET_KEY': flask_secret_key.load_value(),
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
}