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


def show_all_messages(cur, user):
        messages = Messages.load_all_messages(cur, user.id)
        for message in messages:
            from_user = Users.load_user_by_id(cur, message.from_id)
            print(10 * "-")
            print(f"from: {from_user.username}""")
            print(f"data: {message.creation_data}")
            print(message.text)
            print(10 * "-")


def send_message(cur, from_id, recipient_name, text):
        recipient = Users.load_user_by_username(cur, recipient_name)
        if recipient:
            message = Messages(from_id, recipient.id, text=text)
            message.save_to_db(cur)
            print("Message send")
        else:
            print("Recipent does not exists")


if __name__ == '__main__':
    try:
        conn = connect(database="message_server_database", user="postgres", password="coderslab", host="127.0.0.1")
        conn.autocommit = True
        cursor = conn.cursor()
        if args.username and args.password:
            user = Users.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    show_all_messages(cursor, user)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, args.send)
                else:
                    parser.print_help()
            else:
                print("Incorrect password or User does not exist!")
        else:
            print("username and password are required")
            parser.print_help()
        conn.close()
    except OperationalError as err:
        print("Connection Error: ", err)

