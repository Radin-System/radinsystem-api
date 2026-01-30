from ami_client import AMIClient
from zammad_cti import CTIClient
from classmods import ENVMod

ENVMod.load_dotenv()

ami_client = AMIClient(**ENVMod.load_args(AMIClient.__init__))
cti_client = CTIClient(**ENVMod.load_args(CTIClient.__init__))