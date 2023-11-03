import psycopg2
from psycopg2 import Error

def connect_to_db(username, password, host, port, database):
    try:
        connection = psycopg2.connect(user = username,
                                      password = password,
                                      host = host,
                                      port = port,
                                      database = database)
        cursor = connection.cursor()
        print("Connected to DB")
        return cursor, connection
    except (Exception, Error) as error:
        print("Error while connecting to DB")

def disconnect_from_db(connection, cursor):
    if(connection):
        cursor.close()
        connection.close()
        print("Disconnected from DB")
    else:
        print("Connection does not work")

def run_and_fetch_sql(cursor, sql_string):
    try:
        cursor.execute(sql_string)
        record = cursor.fetchall()
        return record
    except (Exception, Error) as error:
        print("Errors while executing SQL")
        return -1