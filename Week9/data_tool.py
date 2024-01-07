#!/usr/bin/env python3

import sys
from collections import defaultdict
import argparse
import logging
import csv
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(
        description='analyze data from specified file.')

    parser.add_argument('fname', metavar='<fname>', type=str,
                    help='file to be processed')

    parser.add_argument('command', type=str, metavar="<command>",
                            help="command to execute",
                            choices=["columns", "values" ])

    parser.add_argument('-c', '--col', dest='columns', metavar='<column name>',
                            action='append', type=str)

    parser.add_argument('-d', '--debug',
                            dest='log_level', action='store_const',
                            const=logging.DEBUG,
                            help='turn on debugging output')

    parser.add_argument('-i', '--info',
                            dest='log_level', action='store_const',
                            const=logging.INFO,
                            help='turn on debugging output')

    args = parser.parse_args()

    if args.log_level is not None:
        logging.getLogger().setLevel(args.log_level)

    run(args)

def run(args):
    print(args)

    with open(args.fname, 'r') as f:
        reader = csv.DictReader(f)

        # process commands
        if args.command == 'columns':
            print("Here are the available columns:")
            for col in reader.fieldnames:
                print(col, end=" | ")
            print("\n")

        elif args.command == 'values':
            if args.columns is None:
                logging.error("Requires column names")
                sys.exit(1)

            for col in args.columns:
                for row in reader:
                    try:
                        print(row[col])
                    except KeyError:
                        logging.error(f"{col} is not a valid key")
                        break


if __name__ == '__main__':
    main()
