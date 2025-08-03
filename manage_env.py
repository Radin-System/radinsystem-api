import application
from classmods import ENVMod


if __name__ == '__main__':
    app = application.create_app(__name__)  # create for ENV load
    ENVMod.save_example()
    ENVMod.sync_env_file()
    ENVMod.load_dotenv()