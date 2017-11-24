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
              "3306 port with requisites from config.py file.")
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
    return result

def get_attr_ids(name):
    '''Return ids of given attribute name'''
    sql = "SELECT id FROM Attribute WHERE name LIKE '%{}%'".format(name)
    result = db_query_all(sql)
    return result

def get_attr_values(attr, server):
    '''Return all values for a given attribute for server'''
    result = []
    for attr_id in get_attr_ids(attr):
        try:
            server_id = get_server_id(server)[0]
            sql = ("SELECT uint_value FROM AttributeValue WHERE "
                   "object_id = {} AND attr_id = {}".format(server_id, attr_id))
            dict_key = db_query_all(sql)[0]
            sql = ("SELECT dict_value FROM Dictionary WHERE dict_key = '{}'"
                       .format(dict_key))
            query = db_query_all(sql)
            if query != ['EMPTY']:
                result.extend(db_query_all(sql))
        except:
            pass
    return result

# def get_fqdn(server_name):
    # '''Return FQDN of the server'''
    # server_id = db_query_all("SELECT id FROM Object WHERE name='{}'"
        # .format(server_name))[0]
    # return server_id
