#!/usr/bin/env python3
import MySQLdb
import re
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
        print("ERROR: Can't connect to database. Check that MySQL is "
              "accessible via 3306 port with requisites from config.py file.")
        sys.exit(30)

def db_close(dbconn, dbcursor):
    '''Close cursor and database connection.'''
    dbcursor.close()
    dbconn.close()

def db_commit(query):
    '''SQL INSERT or UPDATE function.'''
    (dbconn, dbcursor) = db_connect()
    dbcursor.execute(query)
    dbconn.commit()
    db_close(dbconn, dbcursor)

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
    '''Translate server name to its id.'''
    sql = "SELECT id FROM Object WHERE name = '{}'".format(name)
    result = db_query_all(sql)
    return result

def get_attr_ids(name):
    '''Return ids of given attribute name.'''
    if name == 'OS':
        name = "SW type"
    elif name == 'STORAGE':
        name = 'HDD'
    elif name == 'CPU':
        name = 'CPU%Model'
    elif name == 'RAM':
        name = 'DRAM'
    sql = "SELECT id FROM Attribute WHERE name LIKE '%{}%'".format(name)
    result = db_query_all(sql)
    return result

def get_empty_attr_id(name, server):
    '''Return id of the empty attribute slot for a given server.'''
    for attr_id in get_attr_ids(name):
        try:
            server_id = get_server_id(server)[0]
            sql = ("SELECT uint_value FROM AttributeValue WHERE "
                   "object_id = {} AND attr_id = {}".format(server_id, attr_id))
            query = db_query_all(sql)
            if query == []:
                return attr_id
        except:
            pass

def get_attr_values(attr, server):
    '''Return all values for a given attribute for the server.'''
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
        if attr == 'OS':
            result = clean_OS_output(result)
        if attr == 'RAM':
            return dict_key
    return result

def clean_OS_output(array):
    '''Remove unnecessary information from OS names.'''
    result = [re.sub(".*%GSKIP%", "", elem) for elem in array]
    result = [re.sub(" \|.*", "", elem) for elem in result]
    return result

def get_available_values(attr):
    '''Return all possible values for a given attribute.'''
    result = []
    if attr == 'STORAGE':
        chapter_id = 10001
    if attr == 'CPU':
        chapter_id = 10000
    if attr == 'OS':
        chapter_id = 13
    if attr == 'STATUS':
        chapter_id = 10003
    if attr == 'SLA':
        chapter_id = 10004
    sql = ("SELECT dict_value FROM Dictionary WHERE chapter_id = '{}'"
           .format(chapter_id))
    result.extend(db_query_all(sql))
    if attr == 'OS':
        result = clean_OS_output(result)
    return result

def add_attr_value(attr, server, value):
    '''Add a hardware into the server.'''
    try:
        attr_id = get_empty_attr_id(attr, server)
        sql = ("SELECT dict_key FROM Dictionary WHERE dict_value = '{}'"
               .format(value))
        uint_value = db_query_all(sql)[0]
        server_id = get_server_id(server)[0]
        sql = ("INSERT INTO AttributeValue "
               "(object_id, object_tid, attr_id, uint_value) "
               "VALUES ({}, 4, {}, {})".format(server_id, attr_id, uint_value))
        db_commit(sql)
        print('OK')
    except Exception as e:
        print('ERROR: {}'.format(e))
        exit(40)

def set_attr_value(attr, server, value):
    '''Update the value of the specified attribute.'''
    try:
        attr_id = get_attr_ids(attr)[0]
        server_id = get_server_id(server)[0]
        if attr == 'RAM':
            sql = ("UPDATE AttributeValue SET uint_value = {} "
                   "WHERE object_id = {} AND attr_id = {}"
                   .format(value, server_id, attr_id))
        else:
            sql = ("SELECT dict_key FROM Dictionary "
                   "WHERE BINARY dict_value LIKE '%{}%'"
                   .format(value))
            dict_key = db_query_all(sql)[0]
            sql = ("UPDATE AttributeValue SET uint_value = {} "
                   "WHERE object_id = {} AND attr_id = {}"
                   .format(dict_key, server_id, attr_id))
        db_commit(sql)
        print('OK')
    except Exception as e:
        print('ERROR: {}'.format(e))
        exit(40)

def get_last_nonempty_attr_id(attr, server, value):
    '''Return id of the last nonempty attribute for a given server.'''
    for attr_id in reversed(get_attr_ids(attr)):
        try:
            sql = ("SELECT dict_key FROM Dictionary WHERE dict_value = '{}'"
               .format(value))
            uint_value = db_query_all(sql)[0]
            server_id = get_server_id(server)[0]
            sql = ("SELECT * FROM AttributeValue WHERE "
                   "object_id = {} AND attr_id= {} AND uint_value = {}"
                   .format(server_id, attr_id, uint_value))
            query = db_query_all(sql)
            if query != []:
                return attr_id
        except:
            pass

def del_attr_value(attr, server, value):
    '''Remove a hardware from the server.'''
    try:
        attr_id = get_last_nonempty_attr_id(attr, server, value)
        server_id = get_server_id(server)[0]
        sql = ("DELETE FROM AttributeValue "
               "WHERE attr_id = {} AND object_id = {}"
               .format(attr_id, server_id))
        db_commit(sql)
        print('OK')
    except Exception as e:
        print('ERROR: {}'.format(e))
        exit(40)

# def get_fqdn(server_name):
    # '''Return FQDN of the server'''
    # server_id = db_query_all("SELECT id FROM Object WHERE name='{}'"
        # .format(server_name))[0]
    # return server_id
