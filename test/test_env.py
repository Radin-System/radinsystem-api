from classmods import ENVMod
from application.config import Config as _
from ami_client import AMIClient as _


def test_create_env():
    ENVMod.save_example()
    ENVMod.sync_env_file()
