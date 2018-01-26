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
    parser.add_argument('arg', help="Argument for the command.",
        choices=[
            'STORAGE',
            'CPU',
            'FQDN',
            'OS',
            'SERVER',
            'RAM',
            'STATUS'
        ], type=str.upper
    )
    parser.add_argument('-s', '--server', help="Server for the command.")
    parser.add_argument('-v', '--value', help="Value for the command.")
    args = parser.parse_args()

    if (args.command in ['add', 'del']
        and args.arg in ['FQDN', 'OS', 'SERVER', 'RAM']):
        print("ERROR: `{}` and `{}` incompatible."
            .format(args.command, args.arg))
        exit(20)

    if (args.command == 'set'
        and args.arg in ['STORAGE', 'SERVER', 'CPU']):
        print("ERROR: `{}` and `{}` arguments are incompatible."
            .format(args.command, args.arg))
        exit(20)

    if (args.command in ['add', 'del', 'set']
        and args.value is None):
        print("ERROR: `{} {}` requires --value or -v option."
            .format(args.command, args.arg))
        exit(20)

    if (args.arg in
        ['STORAGE', 'CPU', 'OS', 'STATUS']
        and args.server is None):
        print_array(sql.get_available_values(args.arg))
    
    if args.command == 'get':
        if args.arg == 'SERVER':
            print_array(sql.get_servers())
        if args.arg in ['STORAGE', 'CPU', 'OS', 'STATUS']:
            print_array(sql.get_attr_values(args.arg, args.server))
        # if args.arg == 'FQDN':
            # print_array(sql.get_fqdn(args.server))

    if args.command == 'add':
        if args.arg in ['STORAGE', 'CPU']:
            # import pdb; pdb.set_trace()
            sql.add_attr_value(args.arg, args.server, args.value)

    if args.command == 'del':
        if args.arg in ['STORAGE', 'CPU']:
            sql.del_attr_value(args.arg, args.server, args.value)

    if args.command == 'set':
        if args.arg in ['OS', 'STATUS']:
            sql.set_attr_value(args.arg, args.server, args.value)

if __name__ == "__main__":
    main()
