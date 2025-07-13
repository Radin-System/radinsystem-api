from typing import Dict, Optional, Union
from flask import Response, jsonify

JsonSerializable = Union[str, list, dict, tuple, int, float, bool, None]

def create_response(
        data: Optional[Dict[str, JsonSerializable ]] = None,
        message: Optional[str] = None,
        status_code: int = 200,
        **kwargs: JsonSerializable,
    ) -> Response:
    created_data = {
        'ok': True if 200 <= status_code < 400 else False,
        'result': data,
        'message': message,
    }
    created_data.update(kwargs)
    created_data = {k: v for k, v in created_data.items() if v is not None}

    return jsonify(created_data)
