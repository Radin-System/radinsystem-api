from flask import Blueprint, abort, request
from ami_client.operation.action import Login, Logoff, Originate
from ..api_connections import ami_connection
from ..config import ami_configs
from ..utils import create_response

callcenter_bp = Blueprint('callcenter', 'callcenter', url_prefix='/callcenter')

@callcenter_bp.route('/originate', methods=['POST'])
def originate():
    if request.json:
        exten = request.json.get('exten')
        number = request.json.get('number')

    else: abort(415)

    if not exten or not number: abort(400)

    login_request = Login(
        Username=ami_configs['username'],
        Secret=ami_configs['secret'],
        AuthType=ami_configs['auth_type'],
        Events=ami_configs['events'],
    )
    login_request.send(ami_connection)

    originate_response = Originate(
        CallerID=f'Calling: {number}',
        Channel=f'SIP/{exten}',
        Exten=number,
        Context="from-internal",
        Priority="1",
        Timeout="30000",
    ).send(ami_connection, raise_on_no_response=False)
    Logoff().send(ami_connection, raise_on_no_response=False)

    if originate_response:
        return create_response(originate_response._dict)

    else:
        return abort(500)