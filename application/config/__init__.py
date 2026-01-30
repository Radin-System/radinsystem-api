from pathlib import Path
from classmods import ENVMod

class Config:
    def __init__(self) -> None:
        self._flask(**ENVMod.load_args(self.__class__._flask))
        self._logging(**ENVMod.load_args(self.__class__._logging))

    @ENVMod.register(section_name='Flask')
    def _flask(
            self,
            host: str = '127.0.0.1',
            port: int = 8080,
            debug: bool = True,
            secret_key: str = 'SECRET_KEY',
        ) -> None:
        """
        Flask Configurations

        Args:
            host(str): Address to start hosting on
            port(int): Web server port
            debug(bool): Flask debuging
            secret_key(str): Flask Secret key
            mamad(bool): asndoabfubf oqfboqe
        """
        self.flask_host = host
        self.flask_port = port
        self.flask_debug = debug
        self.flask_secret_key = secret_key

    @ENVMod.register(section_name='Log', cast={'file': str})
    def _logging(
            self, 
            level: str = 'INFO',
            file: Path | str = '.log/application.log',
        ) -> None:
        """
        Logging Configurations
        
        Args:
            level(str): Log level (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL)
            file(Path): String or Path Object of application log file.
        """
        self.log_level = level
        self.log_file = file

app_config = Config()
