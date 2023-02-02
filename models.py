from clcrypto import hash_password
from psycopg2 import connect
from psycopg2.errors import OperationalError


class Users:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users (username, hashed_password) 
                    VALUES (%s, %s) RETURNING id"""
            values = (self.username, self._hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        return False

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = """SELECT * FROM users WHERE id=%s"""
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        return None

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = """SELECT * FROM users WHERE username=%s"""
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id
            loaded_user._hashed_password = hashed_password
            return loaded_user
        return None

    @staticmethod
    def load_all_users(cursor):
        sql = """SELECT * FROM users"""
        cursor.execute(sql)
        users = []
        for data in cursor.fetchall():
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = """DELETE FROM Users WHERE id=%s"""
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Messages():
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None

    @property
    def id(self):
        return self._id

    @property
    def creation_data(self):
        return self._creation_date

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO messages (from_id, to_id, text) 
                    VALUES (%s, %s, %s)"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self._creation_date = cursor.fetchone()
            return True
        return False

    @staticmethod
    def load_all_messages(cursor):
        sql = """SELECT * FROM messages"""
        cursor.execute(sql)
        messages = []
        for data in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = data
            loaded_message = Messages(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message._creation_date = creation_date
            messages.append(loaded_message)
        return messages