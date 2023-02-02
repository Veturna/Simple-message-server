import argparse

from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

from clcrypto import check_password
from models import Users


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password')
parser.add_argument('-n', '--new_pass', help='new password')
parser.add_argument('-l', '--list', help='show the user', action='store_true')
parser.add_argument('-d', '--delete', help='delete the user', action='store_true')
parser.add_argument('-e', '--edit', help='edit the user', action='store_true')

args = parser.parse_args()


def create_user(cur, username, password):
    if len(password) < 8:
        print ("Password is too short")
    else:
        try:
            user = Users(username=username, password=password)
            user.save_to_db(cur)
            print ("User created")
        except UniqueViolation:
            print ("User already exists")


def edit_password(username, password, new_pass, cur):
    user = Users.load_user_by_username(cur, username)
    if not user:
        print ("User does not exist")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print ("Password is too short")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cur)
            print ("Password changed")
    else:
        print ("Incorrect password!")


def delete_user(username, password, cur):
    user = Users.load_user_by_username(cursor, username)
    if not user:
        print ("User does not exist")
    elif check_password(password, user.hashed_password):
        user.delete(cur)
        print ("User deleted")
    else:
        print ("Incorrect password!")


def show_all_users(cur):
    users = Users.load_all_users(cur)
    for user in users:
        print(user.username)



if __name__ == '__main__':
    try:
        conn = connect(database="message_server_database", user="postgres", password="coderslab", host="127.0.0.1")
        conn.autocommit = True
        cursor = conn.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_password(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            show_all_users(cursor)
        else:
            parser.print_help()
        conn.close()
    except OperationalError as err:
        print("Connection Error: ", err)