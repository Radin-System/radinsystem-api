import os
from typing import Any, Dict

logging_config: Dict[str, Any] = {
    'log_level': os.environ.get('LOG_LEVEL', 'INFO'),
    'log_file': os.environ.get('LOG_FILE', '.log/application.log'),
}