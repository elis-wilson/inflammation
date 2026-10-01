# Original code: Function that performs a database query
import sqlite3

def connect_to_database(filename):
    return sqlite3.connect(filename)

def query_database(sql, connection=None):

    if connection is None:
        raise TypeError("No databse connection given.")

    # cursor - used to traverse and manipulate results returned by a query
    cursor = connection.cursor()
    # we pass a string named 'sql' that contains our SQL query
    cursor.execute(sql)
    # fetchall - returns a list of tuples containing all rows of our result
    result = cursor.fetchall()
    connection.close()
    return result
