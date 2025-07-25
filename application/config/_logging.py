from classmods import ENVMod
from typing import Any, Dict

log_level = ENVMod.add(
    name = 'level',
    section_name = 'log',
    type_hint = str,
    description = ['Log level for the application.'],
    default = 'INFO',
)
log_file = ENVMod.add(
    name = 'file',
    section_name = 'log',
    type_hint = str,
    description = ['Log file for the application.'],
    default = '.log/application.log',
)

logging_config: Dict[str, Any] = {
    'log_level': log_level.load_value(),
    'log_file': log_file.load_value(),
}