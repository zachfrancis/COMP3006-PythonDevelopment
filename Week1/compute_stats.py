#!/usr/bin/env python3

# Reads numbers from standard input and outputs descriptive statistics
# Meant to be used in conjuction with 'script.sh'

import sys

# List comprehension reading from standard input 
# Ignore entries whose 7 characers are '-9999.0'
avg_temps = [float(num) for num in sys.stdin if num != "-9999.0\n"]

# Data is sorted, so min and max are the first and last entries
min_temp = avg_temps[0]
max_temp = avg_temps[-1]

# Loop over entries to find the average
# I'm avoiding built-ins, so keep a count rather than use len()
sum_temps = 0
count = 0
for num in avg_temps:
    sum_temps += num
    count += 1
avg_temp = sum_temps / count

# Calculate median, also relies on sorted data
idx = count // 2
if (count % 2 == 0):
    median_temp = (avg_temps[idx-1] + avg_temps[idx])/2
else:
    median_temp = avg_temps[idx]

# Print the results as specified
print("min: ", min_temp, ", max: ", max_temp, ", average: ", avg_temp, ", median: ", median_temp, sep='')

