from classmods import ENVMod
from ami_client import AMIClient as _
from zammad_cti import CTIClient as _
import application.config as _


if __name__ == '__main__':
    ENVMod.save_example()
    ENVMod.sync_env_file()
    ENVMod.load_dotenv()