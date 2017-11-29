#!/usr/bin/env python3

import argparse

# Local module, see sql.py file
import sql

'''
API for racktables database.
'''

def print_array(array):
    '''Print array in column'''
    try:
        for i in array:
            print(i)
    except:
        print(array)

def main():
    parser = argparse.ArgumentParser(
        description="A CLI API for racktables database.")
    parser.add_argument('command', help="Command.",
        choices=['get', 'add', 'del', 'set'], type=str.lower)
    parser.add_argument('arg', help="Object for the command.",
        choices=[
            'HDD',
            'CPU',
            'FQDN',
            'OS',
            'TAG',
            'PORT',
            'STATUS',
            'SERVERS'
        ], type=str.upper
    )
    parser.add_argument('-s', '--server', help="Server for the command.")
    parser.add_argument('-v', '--value', help="Value for the command.")
    args = parser.parse_args()

    if (args.arg in
        ['HDD', 'CPU', 'FQDN', 'OS', 'TAG', 'PORT', 'STATUS']
        and args.server is None):
        parser.error("{} requires --server or -s option."
            .format(args.arg))

    if (args.command in ['add', 'del', 'set']
        and args.value is None):
        parser.error("{} requires --value or -v option."
            .format(args.arg))
    
    if args.command == 'get':
        if args.arg.lower() == 'servers':
            print_array(sql.get_servers())
        if args.arg in ['HDD', 'CPU']:
            print_array(sql.get_attr_values(args.arg, args.server))
        # if args.arg == 'FQDN':
            # print_array(sql.get_fqdn(args.server))

    if args.command == 'add':
        if args.arg in ['HDD', 'CPU']:
            sql.add_attr_value(args.arg, args.server, args.value)

if __name__ == "__main__":
    main()
