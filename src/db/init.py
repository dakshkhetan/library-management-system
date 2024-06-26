import mysql.connector

from constants import Constants

try:
    cnx = mysql.connector.connect(user='root',
                                  password='root',
                                  host='127.0.0.1',
                                  database='LIBRARY')

    cursor = cnx.cursor()

except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
