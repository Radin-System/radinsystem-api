from sarvcrm_api import SarvClient
from classmods import ENVMod

sarv_connection = SarvClient(**ENVMod.load_args(SarvClient.__init__))