import time
from flask import Blueprint, redirect, request, url_for

from ..__version__ import __version__
from ..api_connections import netbox_connection
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
            'client-address': request.remote_addr,
            'server-address': request.host,
        }
    )

@diagnose_bp.route('/api-connections')
def api_connections():
    try:
        netbox_version= netbox_connection.version
        netbox_status = 'Connected'
    except:
        netbox_version = None
        netbox_status = 'Not Connected'

    return create_response(
        {
            'netbox': {
                'status': netbox_status,
                'version': netbox_version,
            }
        }
    )