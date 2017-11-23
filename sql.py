#!/usr/bin/env python3
import MySQLdb
import sys

# Local module, see config.py file
import config

'''
Functions for low-level interaction with database.
'''

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
    sqlresult = dbcursor.fetchall()
    result = []
    for i in sqlresult:
        result.append(i[0])
    db_close(dbconn, dbcursor)
    return result

def get_servers():
    '''Get all servers from racktables objects page.'''
    return db_query_all("SELECT name FROM Object WHERE objtype_id=4")

def get_server_id(name):
    '''Translate server name to its id'''
    sql = "SELECT id FROM Object WHERE name = '{}'".format(name)
    result = db_query_all(sql)
    if result != None:
        server_id = result[0]
    else:
        server_id = None
    return server_id

def get_hdds(server_name):
    '''Return all HDD's of the server'''

# def get_fqdn(server_name):
    # '''Return FQDN of the server'''
    # server_id = db_query_all("SELECT id FROM Object WHERE name='{}'"
        # .format(server_name))[0]
    # return server_id
