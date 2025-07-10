import pynetbox

from config import netbox_configs

netbox_connection = pynetbox.api(**netbox_configs)