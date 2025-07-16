import time
from flask import Blueprint, redirect, url_for, request
from ..api_connections import (
    APITester,
    ami_connection,
    netbox_connection,
    sarv_connection
)
from ..utils import create_response, private_addresses_only  

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

@diagnose_bp.route('/api-connections')
@private_addresses_only(request)
def api_connections():
    return create_response(
        {
            'netbox': {
                'message': str(APITester.test_netbox(netbox_connection))
            },
            'ami': {
                'message': str(APITester.test_ami(ami_connection))
            },
            'sarvcrm': {
                'message': str(APITester.test_sarv(sarv_connection))
            },
        }
    )