from typing import Any, Dict, List
from flask import Blueprint, abort, request
from ami_client.operation.action import Originate
from sarvcrm_api import SarvModule
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
        accounts = sarv_connection.Accounts.read_list_all(caching=True)
        contacts = sarv_connection.Contacts.read_list_all(caching=True)

    if request.args.get('type') == 'micro-sip':
        for account in accounts:
            account_numbers = convert_sarv_item_to_mikrosip(sarv_connection, account, 'Account')
            if account_numbers: phonebook += account_numbers

        for contact in contacts:
            contact_numbers = convert_sarv_item_to_mikrosip(sarv_connection, contact, 'Contact')
            if contact_numbers: phonebook += contact_numbers

        return create_response(
            message = f'All contacts from sarvcrm', 
            refresh = 3600,
            items = phonebook,
        )

    elif request.args.get('type') == 'radin-client':
        abort(500)

    else:
        abort(400)

@callcenter_bp.route('/lookup')
@private_addresses_only(request, callcenter_configs.get('phonebook_local_only', False))
def lookup():
    number = request.args.get('number', "")
    lookup_type = request.args.get('type', "")

    if not number and not lookup_type:
        abort(401)

    if lookup_type == 'asterisk':
        with sarv_connection:
            results = sarv_connection.search_by_number(number)

            if not results:
                abort(404)

            module: SarvModule = getattr(sarv_connection, results[0].get('module', 'Accounts'))
            item_id = results[0].get('id', '')
            fullname_en = module.read_record(item_id).get('fullname_en')

        if not fullname_en:
            abort(404)

        return fullname_en

    else:
        abort(401)

@callcenter_bp.route('/originate', methods=['POST'])
@private_addresses_only(request, callcenter_configs.get('phonebook_local_only', False))
def originate():
    if not request.json:
        abort(415)

    exten = request.json.get('exten')
    number = request.json.get('number')        

    if not exten or not number: 
        abort(400)

    Originate(
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

    return create_response({'exten': exten, 'number': number}, message=f'Originate Success')
