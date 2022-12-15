import string
import time
import uuid
import mysql.connector
import hashlib
import random
import conf


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
        sql = "SELECT u.* FROM `Users` u "
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

    def read_auth(self, login, password):
        user = (self.read(login=login) + (None,))[0]
        if user \
                and user.del_dt == None \
                and self.hash_passw(password, user.salt) == user.passw:
            return user
        return None

    def update(self, user: User):
        fields = user.__dict__.keys()
        sql = "UPDATE `users` u SET " + \
            ','.join(f"u.`{field.replace('passw', 'pass')}` = %({field})s" for field in fields if field != 'id') + \
            " WHERE u.`id` = %(id)s "
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, user.__dict__)
            self.db.commit()
        except mysql.connector.Error as err:
            print('update', err)
        else:
            return True
        finally:
            cursor.close()
        return False

    def delete(self, user: User):
        try:
            cursor = self.db.cursor()
            user.del_dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            cursor.execute(
                "UPDATE users u SET u.del_dt = %s WHERE u.id = %s", (user.del_dt, user.id,))
            self.db.commit()
        except mysql.connector.Error as err:
            print('delete', err)
        else:
            return True
        finally:
            try:
                cursor.close()
            except:
                pass
        return False

    def restore(self, user: User):
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE Users u SET u.del_dt = NULL WHERE u.`id` = %s", (user.id))
            self.db.commit()
        except mysql.connector.Error as err:
            print('restore', err)
        else:
            return True
        finally:
            try:
                cursor.close()
            except:
                pass
        return False

    def is_login_free(self, login: str):
        try:
            cursor = self.db.cursor()
        except mysql.connector.Error as err:
            print(err)
        else:
            return not self.read(login=login)
        finally:
            cursor.close()


def main(db_conf):
    try:
        db = mysql.connector.connect(**db_conf)
    except mysql.connector.Error as err:
        print(err.errno, err)
        return
    else:
        print('Connection OK')
        UserDao = UserDAO(db)
        print(UserDao.is_login_free('xxx'))  # False
        print(UserDao.is_login_free('yyy'))  # True


if __name__ == "__main__":
    main(conf.connection)
