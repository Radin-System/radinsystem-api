from classmods import ENVMod
from typing import Dict, Any

callcenter_password = ENVMod.add(
    name = 'password',
    section_name = 'phonebook',
    type_hint = str,
)
callcenter_password_required = ENVMod.add(
    name = 'password_required',
    section_name= 'phonebook',
    type_hint = bool,
    default = 'False',
)
callcenter_local_only = ENVMod.add(
    name = 'local_only',
    section_name = 'phonebook',
    type_hint = bool,
    default = 'False',
)

callcenter_configs: Dict[str, Any] = {
    'phonebook_password': callcenter_password.load_value(),
    'phonebook_password_required': callcenter_password_required.load_value(),
    'phonebook_local_only': callcenter_local_only.load_value(),
}
