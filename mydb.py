import mariadb

connection_info = {
    "host": "localhost",
    "port": 3306,
    "database": "py192",
    "user": "py192_user",
    "password": "pass_192"
}

def main():
    try:
        connection = mariadb.connect(**connection_info)
    except mariadb.Error as err:
        print(err)
    else:
        print("Connection Ok")

if __name__ == "__main__":
    main()