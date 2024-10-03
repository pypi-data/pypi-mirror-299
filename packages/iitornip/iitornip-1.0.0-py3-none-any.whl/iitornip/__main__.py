import argparse
import sys

from . import iitornip
from . import iitornipu
from . import iitornipd


parser = argparse.ArgumentParser(
    description="A Python based tool to check that IP addresses are or are not Tor nodes."
)
parser.add_argument(
    '-i',
    '--ip',
    metavar='IP Address',
    type=str,
    help='The IP address to check.'
)
parser.add_argument(
    '-n',
    '--node',
    default='all',
    metavar='Node Type to check e.g. exit or all',
    type=str,
    help='The type of node to check e.g. exit or all. Default is all. \nIf you want to check all nodes, use all. If you want to check exit nodes, use exit.'
)
parser.add_argument(
    '-u',
    '--update',
    action='store_true',
    help='Update the database. Use this flag in 1 hour only.'
)

args = parser.parse_args()


if args.update:
    update = iitornipu.update_db()
    if update == True:
        print('Database updated successfully.')
    else:
        print('Database update failed. Please try again later.')
    sys.exit()


def cli():
    check = iitornip(args.ip, args.node)
    if check == True:
        print(f'{args.ip} is present in {args.node} Tor node.')
    elif check == False:
        print(f'{args.ip} is not present in {args.node} Tor node.')
    else:
        print(check)
    

if __name__ == '__main__':
    sys.exit(cli())