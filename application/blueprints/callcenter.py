from flask import Blueprint, abort, request
from ami_client.operation.action import Originate
from ..api_connections import ami_connection, sarv_connection
from ..config import callcenter_configs
from ..utils import create_response

callcenter_bp = Blueprint('callcenter', 'callcenter', url_prefix='/callcenter')

# TODO: Configure Local_access only parameter.
@callcenter_bp.route('/phonebook', methods=['GET'])
def phonebook():
    if not (
        request.args.get('password') is not None
        and callcenter_configs.get('phonebook_password_required', False)
        and request.args.get('password') == callcenter_configs.get('phonebook_password', '')
        ):
        abort(401)

    sarv_connection.login()
    contacts = sarv_connection.Contacts.read_list_all()
    contacts_to_send = []

    for contact in contacts:
        firstname = contact.get('first_name', '')
        lastname = contact.get('last_name', '')
        account = contact.get('account_name', '')
        name = f'{firstname}{' '+lastname if lastname else ''}'

        temp = {
            "number": contact.get('primary_number_raw', ''),
            "name": f'{'('+ account +') - ' if account and name not in account else ''}{name}',
            "firstname": firstname,
            "lastname": lastname,
            "email": contact.get('email1', ''),
            "address": contact.get('primary_address_street', ''),
            "city": contact.get('primary_address_city', ''),
            "state": contact.get('primary_address_state', ''),
            "zip": contact.get('primary_address_postalcode', ''),
            "comment": sarv_connection.Contacts.get_url_detail_view(contact.get('id','')),
        }
        temp = {k: v for k, v in temp.items() if v}
        contacts_to_send.append(temp)

    return create_response(
        message = f'All contacts from sarvcrm', 
        refresh = 3600,
        items = contacts_to_send,
    )

@callcenter_bp.route('/originate', methods=['POST'])
def originate():
    if request.json:
        exten = request.json.get('exten')
        number = request.json.get('number')

    else: abort(415)
    if not exten or not number: abort(400)

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

    if originate_response:
        return create_response(originate_response._dict)

    else:
        return abort(500)