import time
from flask import Blueprint, redirect, url_for, request
from ..utils import create_response

diagnose_bp = Blueprint('diagnose', 'diagnose', url_prefix='/diagnose')

@diagnose_bp.route('/test')
def test():
    return create_response(
        {
            'server_time': time.time(),
        }
    )

@diagnose_bp.route('/version')
def version():
    return redirect(url_for('root.version'))

@diagnose_bp.route('/what-is-my-ip')
def what_is_my_ip():
    return create_response(
        {
            'client-address': request.headers.get('X-Real-IP', request.remote_addr),
            'server-address': request.host,
        }
    )
