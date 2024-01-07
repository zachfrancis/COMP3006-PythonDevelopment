#!/usr/bin/env python3

import csv

from collections import namedtuple
from os.path import exists

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
        return self.__repr__()

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
        self._load_data()

    def __iter__(self):
        return iter(self.data)

    def _load_data(self):
        """Open cleaned data file for parsing"""
        if not exists("./autompg.clean.txt"):
            self._clean_data()

        with open("autompg.clean.txt", 'r') as f:
            self.data = self._parse_data(f)

    def _parse_data(self, file):
        """Create AutoMPG objects from each line in file"""
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
            data.append(AutoMPG(make, model, '19' + rec.year, rec.mpg))
        
        return data

    def _clean_data(self):
        """
        Opens 'auto-mpg.data', expands its tabs to spaces, then
        writes cleaned data to a file called 'autompg.clean.txt'
        """
        with open("auto-mpg.data", 'r') as f:
            new_data = []
            for line in f:
                new_data.append(line.expandtabs())
        
        with open("autompg.clean.txt",'w') as f:
            f.writelines(new_data)


def main():
    # Loop through every AutoMPG object created by AutoMPGData
    for a in AutoMPGData():
        print(a)

if __name__ == '__main__':
    main()