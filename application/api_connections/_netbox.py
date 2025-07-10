from pynetbox import api as NetboxClient

from ..config import netbox_configs

netbox_connection = NetboxClient(**netbox_configs)