from typing import Any, Dict, List
from flask import Blueprint, abort, request
from ami_client.operation.action import Originate
from sarvcrm_api import SarvModule
from ..utils import private_addresses_only
from ..connections import ami_client, sarv_client
from ..config import Config
from ..utils import create_response, convert_sarv_item_to_mikrosip


callcenter_bp = Blueprint('callcenter', 'callcenter', url_prefix='/callcenter')


@callcenter_bp.route('/phonebook', methods=['GET'])
@private_addresses_only(request, bool(Config.PHONEBOOK_LOCAL_ONLY.load_value()))
def phonebook():
    if not (
        request.args.get('password') is not None
        and Config.PHONEBOOK_PASSWORD_REQUIRED.load_value()
        and request.args.get('password') == Config.PHONEBOOK_PASSWORD.load_value()
        ):
        abort(401)

    phonebook: List[Dict[str, Any]] = []
    accounts = sarv_client.Accounts.read_all(caching=True)
    contacts = sarv_client.Contacts.read_all(caching=True)

    if request.args.get('type') == 'micro-sip':
        for account in accounts:
            account_numbers = convert_sarv_item_to_mikrosip(sarv_client, account, 'Account')
            if account_numbers: phonebook += account_numbers

        for contact in contacts:
            contact_numbers = convert_sarv_item_to_mikrosip(sarv_client, contact, 'Contact')
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
@private_addresses_only(request, bool(Config.PHONEBOOK_LOCAL_ONLY))
def lookup():
    number = request.args.get('number', "")
    lookup_type = request.args.get('type', "")

    if lookup_type == 'asterisk':
        if not number and not lookup_type:
            return number, 404

        results = sarv_client.search_by_number(number)

        if not results:
            return number, 404

        module: SarvModule = getattr(sarv_client, results[0].get('module', 'Accounts'))
        item_id = results[0].get('id', '')
        fullname_en = module.read_record(item_id).get('fullname_en')

        if not fullname_en:
            return number, 404

        return fullname_en

    else:
        abort(401)

@callcenter_bp.route('/originate', methods=['POST'])
@private_addresses_only(request, bool(Config.PHONEBOOK_LOCAL_ONLY))
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
        ami_client,
        raise_timeout=False,
        raise_on_error_response=False,
        close_connection=True
    )

    return create_response({'exten': exten, 'number': number}, message=f'Originate Success')
