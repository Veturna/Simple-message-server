import argparse

from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

from clcrypto import check_password
from models import Messages, Users

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password')
parser.add_argument('-t', '--to', help='recipient')
parser.add_argument('-s', '--send', help='messages')
parser.add_argument('-l', '--list', help='all messages', action='store_true')

args = parser.parse_args()

def show_all_messages(username, password, cur):
    user = Users.load_user_by_username(username=username)
    if not user:
        print("User does not exist")

def send_message(username, password, cur):
    pass

