from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

sql_create_database = "CREATE DATABASE message_server_database;"

sql_create_users_table = "CREATE TABLE users (id serial PRIMARY KEY, username varchar(255) UNIQUE, " \
                         "hashed_password varchar(80));"

sql_create_messages_table = "CREATE TABLE messages (id serial PRIMARY KEY , " \
                            "from_id integer REFERENCES users(id) ON DELETE CASCADE, " \
                            "to_id integer REFERENCES users(id)) ON DELETE CASCADE, text varchar(255), " \
                            "creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);;"
try:
    conn = connect (host='localhost', user='postgres', password='coderslab')
    conn.autocommit = True
    curs = conn.curor()
    curs.execute(sql_create_database)
except DuplicateDatabase:
    print("Database already exists")
    conn.close()
except OperationalError:
    print("Connection Error")

conn = connect (host='localhost', user='postgres', password='coderslab', dbname='message_server_database')
conn.autocommit = True
curs = conn.curor()

try:
    curs.execute(sql_create_users_table)
except DuplicateTable:
    print("Table already exists")

try:
    curs.execute(sql_create_messages_table)
except DuplicateTable:
    print("Table already exists")
    conn.close()

else:
    conn.close()
    curs.close()

