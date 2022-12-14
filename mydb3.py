import string
import uuid
import mysql.connector
import hashlib
import random


class User:
    def __init__(self, cursor=None):
        if cursor == None:
            self.id = None
            self.login = None
            self.passw = None
            self.name = None
            self.salt = None
            self.avatar = None
            self.email = None
            self.email_code = None
        else:
            row = cursor.fetchone()
            if not row:
                raise ValueError('Cursor has no row(s)')
            u = dict((k, v) for k, v in zip(cursor.column_names, row))
            self.id = u['id']
            self.login = u['login']
            self.passw = u['pass']
            self.name = u['name']
            self.salt = u['salt']
            self.avatar = u['avatar']
            self.email = u['email']
            self.email_code = u['email_code']


class UserDAO:
    def __init__(self, db: mysql.connector.MySQLConnection):
        self.db = db

    def make_salt(self, len: int = 20):
        ''' Generate crypto-salt with 'len' bytes entropy '''
        return random.randbytes(len).hex()

    def hash_pass(self, passw: str, salt: str):
        return hashlib.sha1((passw + salt).encode()).hexdigest()

    def make_email_code(self):
        return ''.join(
            random.choice(string.ascii_lowercase) for i in range(6)
        )

    def create(self, user: User):
        ''' Inserts 'user' into DB table Users'''
        cursor = self.db.cursor()
        user.id = str(uuid.uuid4())
        user.salt = self.make_salt()
        user.passw = self.hash_pass(user.passw, user.salt)
        user.email_code = self.make_email_code()
        # .replace('passw', 'pass')
        keys = user.__dict__.keys()
        sel = ','.join(f"`{x}`" for x in keys).replace('passw', 'pass')
        vals = ','.join(f"%({x})s" for x in keys)
        sql = f'INSERT INTO Users VALUES({vals})'
        try:
            cursor.execute(sql, user.__dict__)
            self.db.commit()
        except mysql.connector.Error as err:
            print(err)
        else:
            print('Create OK')
        finally:
            cursor.close()


def main(db_conf):
    try:
        db = mysql.connector.connect(**db_conf)
    except mysql.connector.Error as err:
        print(err.errno, err)
        return
    print('Connection OK')
    user = User()
    user.name = "Nikita"
    user.login = "xxx"
    user.email = "user@ukr.net"
    user.passw = '1234'
    UserDao = UserDAO(db)
    UserDao.create(user)
    return


if __name__ == "__main__":
    connection_config = {
        "host": "localhost",
        "port": 3306,
        "database": "py192",
        "user": "py192_user",
        "password": "pass_192",
        "use_unicode":                 True,
        "charset":            "utf8mb4",
        "collation": "utf8mb4_general_ci"
    }
    main(connection_config)
