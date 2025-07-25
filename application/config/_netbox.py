from classmods import ENVMod
from typing import Dict, Any

netbox_url = ENVMod.add(
    name = 'url',
    section_name = 'netbox',
    type_hint = str,
    required = True,
)
netbox_token = ENVMod.add(
    name = 'token',
    section_name = 'netbox',
    type_hint = str,
    required = True,
)

netbox_configs: Dict[str, Any] = {
    'url': netbox_url.load_value(),
    'token': netbox_token.load_value(),
}