#!/usr/bin/env python3

import argparse

# Local module, see sql.py file
import sql

'''
API for racktables database.
'''

def get_servers():
    return sql.get_servers()

def print_array(array):
    '''Print array in column'''
    try:
        for i in array:
            print(i)
    except:
        print(array)

def main():
    parser = argparse.ArgumentParser(description="A CLI API for racktables database.")
    parser.add_argument('command', choices=['get_servers', 'get_hdds'], help="Command.")
    parser.add_argument('-s', '--server', help="Server for the command.")
    args = parser.parse_args()
    if args.command == 'get_hdds' and args.server is None:
        parser.error("get_hdds requires --server or -s")
    if args.command == 'get_servers':
        print_array(get_servers())

if __name__ == "__main__":
    main()
