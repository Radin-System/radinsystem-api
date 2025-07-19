from typing import Any, List, Dict, Literal
from copy import deepcopy
from sarvcrm_api import SarvClient


def convert_sarv_item_to_mikrosip(
        item: dict,
        item_type: Literal['Account', 'Contact', 'User']
    ) -> List[Dict[str, Any]] | None:

    if int(item.get('deleted', 0)): return
    display_name = ''
    firstname = item.get('first_name', '')
    lastname = item.get('last_name', '')
    fullname = f'{firstname}{' '+lastname if lastname else ''}'

    if item_type == 'Account':
        display_name = f'({item.get('name', '')})'

    elif item_type == 'Contact':
        account = item.get('account_name', '')
        display_name = f'{'('+ account +') - ' if account and fullname not in account else ''}{fullname}'

    elif item_type == 'User':
        fullname = f'{firstname}{' '+lastname if lastname else ''}'
        display_name = fullname

    else:
        raise ValueError('item_type must be one of these: `Account`, `Contact`, `User`')

    template = {
        "name": display_name,
        "firstname": firstname,
        "lastname": lastname,
        "email": item.get('email1', ''),
        "address": item.get('primary_address_street', ''),
        "city": item.get('primary_address_city', ''),
        "state": item.get('primary_address_state', ''),
        "zip": item.get('primary_address_postalcode', ''),
        "comment": f'{item_type} - {item.get('id')}',
    }
    template = {k: v for k, v in template.items() if v}

    numbers = []
    for raw_number in item.get('numbers', []):
        number_item = deepcopy(template)
        new_number = raw_number.get('number')
        if new_number:
            number_item['number'] = new_number
            number_item['name'] = number_item['name'] + ' - ' + new_number
            for x in numbers:
                if x['number'] == new_number: continue

            numbers.append(number_item)

    return numbers