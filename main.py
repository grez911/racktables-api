#!/usr/bin/env python3

# Local module, see sql.py file
import sql

'''
API for racktables database.
'''

def get_all_servers():
    return sql.get_all_servers

def pretty_print(array):
    '''Print array in column'''
    try:
        for i in array:
            print(i)
    except:
        print(array)

def main():
    pass

if __name__ == "__main__":
    main()
