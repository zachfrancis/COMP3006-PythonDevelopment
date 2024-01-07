#!/usr/bin/env python3

import csv
import logging
import requests
import argparse
import sys

from collections import namedtuple
from os.path import exists

### BEGIN LOGGING SETUP ###
logger = logging.getLogger("autompg2")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s][%(asctime)s][%(name)s] %(message)s')

# Add handler for stdout
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)

# Add handler for logging to a file
fh = logging.FileHandler(filename='autompg2.log', mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
### END LOGGING SETUP ###

Record = namedtuple('Record', ['mpg','cylinders','displacement','horsepower','weight',
                               'acceleration','year','origin','make_model'])

class AutoMPG:
    """Class to represent a single automobile record"""
    def __init__(self, make, model, year, mpg):
        self.make = str(make)
        self.model = str(model) 
        self.year = int(year)
        self.mpg = float(mpg)

    def __repr__(self):
        return f"AutoMPG('{self.make}','{self.model}','{self.year}','{self.mpg}')"

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if type(self) == type(other):
            return (self.make, self.model, self.year, self.mpg) == \
                   (other.make, other.model, other.year, other.mpg)
        return NotImplemented

    def __lt__(self, other):
        if type(self) == type(other):
            return (self.make, self.model, self.year, self.mpg) < \
                   (other.make, other.model, other.year, other.mpg)
        return NotImplemented

    def __hash__(self):
        return hash(self.make, self.model, self.year, self.mpg)

class AutoMPGData:
    """Class for handling automobile data"""
    def __init__(self):
        logger.debug("Initializing AutoMPGData")
        self._load_data()

    def __iter__(self):
        return iter(self.data)

    def _get_data(self):
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
        req = requests.get(url)
        logger.info("Accessed URL: " + url + " Response status: " + str(req.status_code))
        req.raise_for_status()
        return req.text

    def _load_data(self):
        """Open cleaned data file for parsing"""
        if not exists("./autompg.clean.txt"):
            with open('auto-mpg.data','w') as f:
                f.write(self._get_data())

        if not exists("./autompg.clean.txt"):
            self._clean_data()

        with open("autompg.clean.txt", 'r') as f:
            self.data = self._parse_data(f)

    def _parse_data(self, file):
        """Create AutoMPG objects from each line in file"""
        logger.info("Parsing AutoMPG Data...")
        reader = csv.reader(file, delimiter=' ', skipinitialspace=True)
        data = []
        for row in reader:
            rec = Record(*row) # Unpack row into Record namedtuple 
            
            # Make is first, anything else split from the string is part of model
            # Cannot ust split(' ', maxsplit=1) for entries that just have the make
            make_info = rec.make_model.split(' ')
            make = make_info[0]
            model = ' '.join(make_info[1:])

            # Assumes every year is prefixed with 19 (no cars beyond 2000)
            autompg = AutoMPG(make, model, '19' + rec.year, rec.mpg)
            logger.debug("Adding " + str(autompg) + "to the table")
            data.append(autompg)
        
        return data

    def _clean_data(self):
        """
        Opens 'auto-mpg.data', expands its tabs to spaces, then
        writes cleaned data to a file called 'autompg.clean.txt'
        """
        logger.info("Creating a clean data file...")
        with open("auto-mpg.data", 'r') as input:
            with open("autompg.clean.txt",'w') as output:
                for line in input:
                    output.write(line.expandtabs())

    def sort_by_default(self):
        logger.info("Sorting Auto MPG data by make (default sort)...")
        list.sort(self.data)

    def sort_by_year(self):
        logger.info("Sorting Auto MPG data by year...")
        list.sort(self.data, key=lambda auto : (auto.year, auto.make, auto.model, auto.mpg))

    def sort_by_mpg(self):
        logger.info("Sorting Auto MPG data by MPG...")
        list.sort(self.data, key=lambda auto : (auto.mpg, auto.make, auto.model, auto.year))


def main():
    parser = argparse.ArgumentParser(description='analyze Auto MPG data set')
    parser.add_argument('command', metavar='<command>', type=str, help='command to execute', choices=['print'])
    parser.add_argument('-s', '--sort', dest='sort_type', action='store', metavar='<sort order>', 
                        choices=['year', 'mpg', 'default'])
    args = parser.parse_args()

    logger.info("Arguments provided: " + str(sys.argv[1:]))

    a = AutoMPGData()

    if args.sort_type == 'year':
        a.sort_by_year()
    elif args.sort_type == 'mpg':
        a.sort_by_mpg()
    elif args.sort_type == 'default':
        a.sort_by_default()

    if args.command == 'print':
        for auto in a:
            print(auto)

if __name__ == '__main__':
    main()