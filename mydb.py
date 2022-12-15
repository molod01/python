import mysql.connector
import conf


def show_databases(connection: mysql.connector.MySQLConnection):
    cursor = connection.cursor()
    sql = "SHOW DATABASES"
    cursor.execute(sql)
    print("> DATABASES")
    print(", ".join(row[0] for row in cursor), end='\n\n')


def show_tables(connection: mysql.connector.MySQLConnection):
    cursor = connection.cursor()
    sql = "SHOW TABLES"
    cursor.execute(sql)
    print("> TABLES")
    print(", ".join(row[0] for row in cursor), end='\n\n')


def main():
    try:
        connection = mysql.connector.connect(**conf.connection)
    except mysql.connector.Error as err:
        print(err)
    else:
        print("Connection Ok")
    show_databases(connection)
    show_tables(connection)


if __name__ == "__main__":
    main()
