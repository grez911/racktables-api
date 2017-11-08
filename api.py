#!/usr/bin/env python3
import MySQLdb
import sys
import re
import ipaddr

import config

def db_connect():
    try:
        return MySQLdb.connect(
            host=config.host,
            port=config.port,
            passwd=config.passwd,
            db=config.db,
            user=config.user)
    except:
        print("Can't connect to database. Check that MySQL is accessible via "
            + "3306 port with requisites from config.py file")
        sys.exit(1)

db = db_connect()
db.db_query_all("SELECT name FROM Object")
r = db.store_result()
print(r)
