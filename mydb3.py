import string
import uuid
import mysql.connector
import hashlib
import random


class User:

    def __init__(self, row=None) -> None:
        if row == None:
            self.id = None
            self.login = None
            self.passw = None
            self.name = None
            self.salt = None
            self.avatar = None
            self.email = None
            self.email_code = None
        elif isinstance(row, dict):
            self.id = row["id"]
            self.login = row["login"]
            self.passw = row["pass"]
            self.name = row["name"]
            self.salt = row["salt"]
            self.avatar = row["avatar"]
            self.email = row["email"]
            self.email_code = row["email_code"]
        else:
            raise ValueError("row type unsuppotred")

    def __str__(self) -> str:
        return str(self.__dict__)

    __repr__ = __str__


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

    def read(self, id=None, login=None):
        ''' Read all 'users' from DB table Users'''
        sql = f"SELECT u.* FROM `Users` u "
        params = []
        if id:
            sql += "WHERE u.`id` = %s "
            params.append(id)
        if login:
            sql += ("AND" if id else "WHERE ") + "u.`login` = %s "
            params.append(login)
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(sql, params)
        except mysql.connector.Error as err:
            print(err)
        else:
            return tuple(User(row) for row in cursor)
        finally:
            cursor.close()

    def read_auth(self, login, password) -> User | None:
        user = (self.read(login=login) + (None,))[0]
        if user and self.hash_pass(password, user.salt) == user.passw:
            return user
        return None


def main(db_conf):
    try:
        db = mysql.connector.connect(**db_conf)
    except mysql.connector.Error as err:
        print(err.errno, err)
        return
    print('Connection OK')
    UserDao = UserDAO(db)
    # user = User()
    # user.name = "Nikita"
    # user.login = "xxx"
    # user.email = "user@ukr.net"
    # user.passw = '1234'
    # UserDao.create(user)
    print(UserDao.read_auth('xxx', '1234'))
    print(UserDao.read(login='xxx'))

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
