from ami_client import AMIClient
from classmods import ENVMod

ami_client = AMIClient(**ENVMod.load_args(AMIClient.__init__))
