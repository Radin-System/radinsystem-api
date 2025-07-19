from typing import Any, Dict, List
from flask import Blueprint, abort, request
from ami_client.operation.action import Originate
from ..utils import private_addresses_only
from ..api_connections import ami_connection, sarv_connection
from ..config import callcenter_configs
from ..utils import create_response, convert_sarv_item_to_mikrosip


callcenter_bp = Blueprint('callcenter', 'callcenter', url_prefix='/callcenter')

@callcenter_bp.route('/phonebook', methods=['GET'])
@private_addresses_only(request, callcenter_configs.get('phonebook_local_only', False))
def phonebook():
    if not (
        request.args.get('password') is not None
        and callcenter_configs.get('phonebook_password_required', False)
        and request.args.get('password') == callcenter_configs.get('phonebook_password', '')
        ):
        abort(401)

    phonebook: List[Dict[str, Any]] = []

    with sarv_connection:
        users = sarv_connection.Users.read_list_all(caching=True)
        accounts = sarv_connection.Accounts.read_list_all(caching=True)
        contacts = sarv_connection.Contacts.read_list_all(caching=True)

    if request.args.get('type') == 'micro-sip':
        for user in users:
            user_numbers = convert_sarv_item_to_mikrosip(user, 'User')
            #if user_numbers: phonebook += user_numbers

        for account in accounts:
            account_numbers = convert_sarv_item_to_mikrosip(account, 'Account')
            if account_numbers: phonebook += account_numbers

        for contact in contacts:
            contact_numbers = convert_sarv_item_to_mikrosip(contact, 'Contact')
            #if contact_numbers: phonebook += contact_numbers

        return create_response(
            message = f'All contacts from sarvcrm', 
            refresh = 3600,
            items = phonebook,
        )

    if request.args.get('type') == 'radin-client':
        abort(500)

    else:
        abort(400)

@callcenter_bp.route('/originate', methods=['POST'])
@private_addresses_only(request, callcenter_configs.get('phonebook_local_only', False))
def originate():
    if not request.json:
        abort(415)

    exten = request.json.get('exten')
    number = request.json.get('number')        

    if not exten or not number: 
        abort(400)

    originate_response = Originate(
        CallerID=f'Calling: {number}',
        Channel=f'SIP/{exten}',
        Exten=number,
        Context="from-internal",
        Priority="1",
        Timeout="30000",
    ).send(
        ami_connection,
        raise_timeout=False,
        raise_on_error_response=False,
        close_connection=True
    )

    if not originate_response:
        return abort(500)

    return create_response(originate_response._dict)
