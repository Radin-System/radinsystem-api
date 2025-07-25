from ami_client import AMIClient
from classmods import ENVMod

ami_connection = AMIClient(**ENVMod.load_args(AMIClient.__init__))