from operator import ge
from os import environ

from mysql.connector import connect, Error

try: 
    with connect(
        host = environ.get('sql_server'),
        user = environ.get('sql_login'),
        password = environ.get('sql_password')
    ) as connection: 
        print(connection)

except Error as e:
    print(e)

    