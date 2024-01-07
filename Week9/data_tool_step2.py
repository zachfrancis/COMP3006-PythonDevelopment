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
                            choices=["columns", "values"])
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
    parser.add_argument('-n', dest='n_rows', default=-1, type=int,
                            help='limit the number of rows displayed')

    parser.add_argument('-p', '--plot',
                            dest='do_plot', action='store_true',
                            help='plot the data')
    
    args = parser.parse_args()

    if args.log_level is not None:
        logging.getLogger().setLevel(args.log_level)

    run(args)

def check_columns(args):
    if args.columns is None:
        raise ValueError(f'{args.command} command requires at least one column name')

def print_row(values, sep=False):
    # print the header row
    first = True
    for value in values:
        if not first:
            print("\t", end='')
        else:
            first = False
        print(value, end='')

    print() #end of line

    if sep:
        print("=" * 80)

def run(args):
    logging.debug(args)

    # all commands need the file open...
    with open(args.fname, 'r') as f:
        reader = csv.DictReader(f)

        # process commands
        if args.command == 'columns':
            print_row(["Column Names"], True)
            for name in reader.fieldnames:
                print_row([name])

        elif args.command == 'values':
            check_columns(args)
            print_row(args.columns, True)
            n = 1
            for row in reader:
                values = []
                for col in args.columns:
                    values.append(row[col])
                print_row(values)
                n += 1
                if args.n_rows > 0 and n > args.n_rows:
                    break



if __name__ == '__main__':
    main()

