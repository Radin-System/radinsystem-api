from ami_client import AMIClient
from pynetbox import api as NetboxClient
from sarvcrm_api import SarvClient
from classmods import return_exception_on_error

class APITester:
    @staticmethod
    @return_exception_on_error
    def test_ami(ami: AMIClient) -> str | Exception:
        raise NotImplementedError('No implementation provided from AMIClient')
    
    @staticmethod
    @return_exception_on_error
    def test_netbox(netbox: NetboxClient) -> str | Exception:
        return netbox.version

    @staticmethod
    @return_exception_on_error
    def test_sarv(sarv: SarvClient) -> str | Exception:
        sarv.login()
        return "v'5.0.0'" if sarv.url.endswith("API.php") else sarv.url.split('/')[5].replace('_', '.')
