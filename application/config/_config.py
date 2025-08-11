from classmods import ENVMod


PHONEBOOK_PASSWORD = ENVMod.add(
    name = 'password',
    section_name = 'phonebook',
    type_hint = str,
)
PHONEBOOK_PASSWORD_REQUIRED = ENVMod.add(
    name = 'password_required',
    section_name= 'phonebook',
    type_hint = bool,
    default = 'False',
)
PHONEBOOK_LOCAL_ONLY = ENVMod.add(
    name = 'local_only',
    section_name = 'phonebook',
    type_hint = bool,
    default = 'False',
)
FLASK_HOST = ENVMod.add(
    name = 'host',
    section_name = 'flask',
    type_hint = str,
    default = '127.0.0.1',
)
FLASK_PORT = ENVMod.add(
    name = 'port',
    section_name = 'flask',
    type_hint = int,
    default = '8080',
)
FLASK_DEBUG = ENVMod.add(
    name = 'debug',
    section_name = 'flask',
    type_hint = bool,
    default = 'True',
)
FLASK_SECRET_KEY = ENVMod.add(
    name = 'secret_key',
    section_name = 'flask',
    type_hint = str,
    required = True,
)
LOG_LEVEL = ENVMod.add(
    name = 'level',
    section_name = 'log',
    type_hint = str,
    description = ['Log level for the application.'],
    default = 'INFO',
)
LOG_FILE = ENVMod.add(
    name = 'file',
    section_name = 'log',
    type_hint = str,
    description = ['Log file for the application.'],
    default = '.log/application.log',
)
NETBOX_URL = ENVMod.add(
    name = 'url',
    section_name = 'netbox',
    type_hint = str,
    required = True,
)
NETBOX_TOKEN = ENVMod.add(
    name = 'token',
    section_name = 'netbox',
    type_hint = str,
    required = True,
)
TELEGRAM_TOKEN = ENVMod.add(
    name = 'token',
    section_name = 'telegram',
    type_hint = str,
    required = True,
)
TELEGRAM_CHAT_ID = ENVMod.add(
    name = 'chat_id',
    section_name = 'telegram',
    type_hint = str,
    required = True,
)
TELEGRAM_TICKET_THREAD = ENVMod.add(
    name = 'thread',
    section_name = 'telegram',
    type_hint = str,
)