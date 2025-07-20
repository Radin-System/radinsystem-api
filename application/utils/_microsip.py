import persian
from sarvcrm_api import SarvClient
from typing import Any, List, Dict, Literal, Set
from copy import deepcopy


def convert_sarv_item_to_mikrosip(
        clinet: SarvClient,
        item: dict,
        item_type: Literal['Account', 'Contact']
    ) -> List[Dict[str, Any]] | None:
    if int(item.get('deleted', 0)): return
    display_name = ''
    firstname = item.get('first_name', '')
    lastname = item.get('last_name', '')
    fullname = f'{firstname}{' '+lastname if lastname else ''}'

    if item_type == 'Account':
        display_name = f'({item.get('name', '')})'
        link = clinet.Accounts.get_url_detail_view(item.get('id', '')) if item.get('id') else ''

    elif item_type == 'Contact':
        account = item.get('account_name', '')
        display_name = f'{'('+ account +') - ' if account and fullname not in account else ''}{fullname}'
        link = clinet.Contacts.get_url_detail_view(item.get('id', '')) if item.get('id') else ''

    else:
        raise ValueError('item_type must be one of these: `Account`, `Contact`, `User`')

    template = {
        "name": display_name,
        "firstname": firstname,
        "lastname": lastname,
        "email": item.get('email1', ''),
        "address": link,
        "comment": f'{item_type} - {item.get('id')}',
    }
    template = {k: v for k, v in template.items() if v}

    phonebook_items: List[Dict[str, Any]] = []
    all_numbers: Set[str] = {persian.convert_fa_numbers(x.get('number').strip()) for x in item.get('numbers', []) if x.get('number')}
    for number in all_numbers:
        phonebook_item = deepcopy(template)
        phonebook_item['number'] = number
        phonebook_item['name'] += ' - '+number
        phonebook_items.append(phonebook_item)

    return phonebook_items