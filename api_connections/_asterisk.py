from ami_client import AMIClient
from ami_client.operation.action import Login

from config import ami_configs

ami_connection = AMIClient(
    host = ami_configs['host'],
    port = ami_configs['port'],
)

Login()