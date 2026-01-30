from flask import Blueprint, abort, request
from ami_client.operation.action import Originate
from ..utils import private_addresses_only
from ..connections import ami_client
from ..utils import create_response

callcenter_bp = Blueprint('callcenter', 'callcenter', url_prefix='/callcenter')

@callcenter_bp.route('/originate', methods=['POST'])
@private_addresses_only(request)
def originate():
    if not request.json:
        abort(415)

    exten = request.json.get('exten')
    number = request.json.get('number')

    if not exten or not number: 
        abort(400)

    ami_client.send_action(
        Originate(
            CallerID=f'Calling: {number}',
            Channel=f'SIP/{exten}',
            Exten=number,
            Context="from-internal",
            Priority="1",
            Timeout="30000",
        ),
        check_connection=True,
        check_authentication=True,
        close_connection=(not ami_client.is_connected()),
    )

    return create_response(
        data={'exten': exten, 'number': number}, 
        message=f'Originate Success'
    )
