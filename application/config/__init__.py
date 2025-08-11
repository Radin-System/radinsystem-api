from classmods import ENVMod
ENVMod.load_dotenv()

from . import _config as Config

__all__ = [
    'Config',
]