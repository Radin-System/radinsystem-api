from pynetbox import api as NetboxClient
from ..config import Config


netbox_client = NetboxClient(
    url = Config.NETBOX_URL.load_value(),
    token = Config.NETBOX_TOKEN.load_value(),
)
