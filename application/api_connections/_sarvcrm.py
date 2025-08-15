from sarvcrm_api import SarvClient
from classmods import ENVMod


sarv_client = SarvClient(**ENVMod.load_args(SarvClient.__init__))
