import argparse
from psycopg2 import connect
from clcrypto import check_password
from models import Users


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password')
parser.add_argument('-n', '--new_pass', help='new password')
parser.add_argument('-l', '--list', help='show the user')
parser.add_argument('-d', '--delete', help='delete the user')
parser.add_argument('-e', '--edit', help='edit the user')

args = parser.parse_args()


def create_the_user():
    pass

def edit_the_password():
    pass

def delete_the_password():
    pass

def show_the_user():
    pass

def print_help():
    pass


if __name__ == '__main__':
    cnx = connect(database="message_server_database", user="postgres", password="postgres", host="127.0.0.1")
    cnx.autocommit = True
    cursor = cnx.cursor()