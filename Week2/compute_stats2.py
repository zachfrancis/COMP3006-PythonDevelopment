#!/usr/bin/env python3

import sys
import csv
from typing import List, Tuple

def main():

    if (len(sys.argv) < 2):
        print("Not enough arguments provided")
        sys.exit(1)

    try:
        # First argument what numbered column will be analyzed
        col = int(sys.argv[1]) - 1
    except ValueError:
        print("First argument must be an INT of desired column")
        sys.exit(1)

    # Single argument is a column number, data read from stdin
    # Two arguments is a column followed by name of a csv file (space delimited)
    if (len(sys.argv) == 2):
        reader = csv.reader(sys.stdin, delimiter=' ', skipinitialspace=True)
        data = [float(row[col]) for row in reader if row[col] != '-9999.0' and row[col] != '-99.000']
    else:
        with open("Data.txt","r") as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', skipinitialspace=True)
            data = [float(row[col]) for row in reader if row[col] != '-9999.0' and row[col] != '-99.000']

    # compute_stats() only accepts sorted data 
    data.sort()
    (min_temp, max_temp, avg_temp, median_temp) = compute_stats(data)
    print("min: ", min_temp, ", max: ", max_temp, ", average: ", avg_temp, ", median: ", median_temp, sep='')


def compute_stats(values: List) -> Tuple:
    """Return min, max, average, and median values of sorted list"""

    if (values is None or len(values) == 0):
        return (None, None, None, None)

    values_len = len(values)

    # Data is sorted, min and max are first and last values
    o_min = values[0]
    o_max = values[-1]

    # Calculate average
    o_sum = 0
    for num in values:
        o_sum += num
    o_avg = o_sum / values_len

    # Calculate median
    idx = values_len // 2
    if (values_len % 2 == 0):
        o_median = (values[idx-1] + values[idx])/2
    else:
        o_median = values[idx]

    return (o_min, o_max, o_avg, o_median)

if __name__ == '__main__':
    main()