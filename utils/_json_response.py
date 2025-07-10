from typing import Optional
from flask import Response, jsonify


def create_response(data: Optional[dict] = None, message: Optional[str] = None, status_code: int = 200) -> Response:
    created_data = {
        'ok': True,
        'result': data,
        'message': message,
        'code': status_code,
    }
    created_data = {k: v for k, v in created_data.items() if v is not None}

    return jsonify(created_data)
