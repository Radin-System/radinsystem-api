from typing import Literal, Optional

URI_SCHEME = Literal['SQLITE', 'MSSQL', 'MYSQL', 'POSTGRE', 'MARIADB']

def create_database_uri(
        scheme: URI_SCHEME,
        database: Optional[str],
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> str:
    
    connection_auth = f'{username}:{password}@{host}:{port}/{database}'

    if scheme == 'SQLITE':
        connection_scheme = 'sqlite'
        connection_auth = '/' + (database if database is not None else 'database') + '.db'

    elif scheme == 'MSSQL':
        connection_scheme = 'mssql+pyodbc'
    
    elif scheme == 'MYSQL':
        connection_scheme = 'mysql+mysqlconnector'
    
    elif scheme == 'POSTGRE':
        connection_scheme = 'postgresql+psycopg2'
    
    elif scheme == 'MARIADB':
        connection_scheme = 'mysql+pymysql'
    
    else:
        raise AttributeError(
            f'Scheme not supported: {scheme}'
        )

    return f'{connection_scheme}://{connection_auth}'