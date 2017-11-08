#!/usr/bin/env python3
import MySQLdb
import sys
import re
import ipaddr

import config

def db_connect():
    '''Connect to the database, return MySQLdb.connect object and cursor.'''
    try:
        dbconn = MySQLdb.connect(
            host=config.host,
            port=config.port,
            passwd=config.passwd,
            db=config.db,
            user=config.user)
        dbcursor = dbconn.cursor()
        return (dbconn, dbcursor)
    except:
        print("Can't connect to database. Check that MySQL is accessible via "
            + "3306 port with requisites from config.py file.")
        sys.exit(1)

def db_close(dbconn, dbcursor):
    '''Close cursor and database connection.'''
    dbcursor.close()
    dbconn.close()

def db_query_all(query):
    '''SQL query function, return all rows.'''
    (dbconn, dbcursor) = db_connect()
    dbcursor.execute(query)
    result = dbcursor.fetchall()
    db_close(dbconn, dbcursor)
    return result

def get_all_servers():
    '''Get all servers from racktables objects page.'''
    sqlresult = db_query_all("SELECT name FROM Object WHERE objtype_id=4")
    result = []
    for i in sqlresult:
        result.append(i[0])
    return result

def pretty_print(array):
    '''Print array in column'''
    for i in array:
        print(i)

def main():
    pretty_print(get_all_servers())

if __name__ == "__main__":
    main()
