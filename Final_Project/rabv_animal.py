#!/usr/bin/env python3
import csv
import logging
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse


class AnimalRABVData:
    def __init__(self):
        self._load_file()


    def __repr__(self):
        return 'Animal rabies cases, China: 2003 - 2018'


    def __iter__(self):
        return iter(self.data)


    def _load_file(self):
        '''opens datafile, cleans and targets data from 2003 and on in China. returns list of lists comprised of location in China cases were counted, type of animal that had rabies, year animal had rabies, and the viral clade identified in the animal'''
        self.data = []
        logging.debug('opening file')
        f_in = open('rabv_animal.csv')
        reader = csv.reader(f_in, delimiter=',', skipinitialspace=True)
        logging.info('file opened')

        for line in reader:
            if 'China' in line[0] and int(line[4]) >= 2003:
                location = str(line[1].replace('\xa0', ''))
                animal = str(line[3].replace('\xa0', ''))
                year = int(line[4].replace('\xa0', ''))
                clade = str(line[5].replace('\xa0', ''))
                self.data.append([location, animal, year, clade])


    def cases_per_year(self):
        '''counts the total animal cases per year and returns a tuple of year as index 0 and total as index 1'''
        logging.debug('counting cases per year between 2003 and 2008 in China')

        year_list = []
        for item in self.data:
            year_list.append(item[2])
        ctr = Counter(year_list)
        return ctr


    def clade(self):
        '''counts the total viral clades identified in all animal species per year and returns a tuple of year as index 0 and total as index 1'''
        clade_list = []
        logging.debug('counting viral clades')
        for item in self.data:
            clade_list.append(item[3])
        return Counter(clade_list)


    def animal_counts(self):
        '''counts the number of cases for each animal species and returns a dictionary with animal species as key and count as value'''
        animals = ['Dog', 'Cattle', 'Pig', 'Sheep', 'Camel', 'Fox', 'Raccoon dog', 'Deer', 'Ferret badger']
        logging.debug('counting animal species')
        animal_list = []
        for item in self.data:
            animal_list.append(item[1])
        animal_ctr = Counter(animal_list)
    
        #clean data for dictionary (i.e. no animal listed or 'vaccine' listed as animal)
        logging.debug('cleaning animal species')
        return {k: animal_ctr[k] for k in animals}

    
    def sep_wild_dom(self):
        domestic = ['Dog', 'Cattle', 'Pig', 'Sheep', 'Camel']
        dDict = defaultdict(int)
        for x in range(2003,2019):
            dDict[x]
        for line in self.data:
            for key in dDict:
                if line[2] == key and line[1] in domestic:
                    dDict[key] += 1

        x_yr = []
        y_dom = []
        for key, value in dDict.items():
            x_yr.append(key)
            y_dom.append(value)

        wDict = defaultdict(int)
        wild = ['Fox', 'Raccoon dog', 'Deer', 'Ferret badger']
        y_wild = []
        for x in range(2003,2019):
            wDict[x]
        for line in self.data:
            for key in dDict:
                if line[2] == key and line[1] in wild:
                    wDict[key] += 1

        for key, value in wDict.items():
            y_wild.append(value)
        return (x_yr, y_dom, y_wild)


    def data_structures(self):
        '''structures the data in preparation for plotting'''
        logging.debug('structuring data for analysis')

        #sorting years in chronological order and creating lists to be plotted as x and y for total cases per year
        ordered_years = sorted(self.cases_per_year().items())
        x_yr_all = []
        y_yr_all = []

        for year_count_pair in ordered_years:
            year, count = year_count_pair
            x_yr_all.append(year)
            y_yr_all.append(count)

        #sorting years in chronological order and creating lists to be plotted as x and y for total cases per year
        #NOTE: maybe this is a place to use numpy
        clade_ctr = self.clade()
        x_clade = list(clade_ctr.keys())
        y_clade = list(clade_ctr.values())
        return ((x_yr_all, y_yr_all), (x_clade, y_clade))


    def general_stats(self, stats_outfile, args):
        '''conducts basic statistical analysis to produce a summary that can be printed to the console or output in a file'''
        logging.debug('calculating general statistics')
        
        year_ctr = self.cases_per_year()
        years, clades = self.data_structures()
        x_yr_all, y_yr_all = years

        max_year = max(year_ctr, key=year_ctr.get) 
        max_value = year_ctr[max_year] 

        min_year = min(year_ctr, key=year_ctr.get) 
        min_value = year_ctr[min_year] 

        total_cases = sum(y_yr_all) 

        avg_year = total_cases/len(year_ctr) 

        clade_ctr = self.clade()

        unique_clades = len(clade_ctr) 
        max_clade = max(clade_ctr, key=clade_ctr.get) 
        max_value = clade_ctr[max_clade] 

        min_clade = min(clade_ctr, key=clade_ctr.get) 
        min_value = clade_ctr[min_clade] 

        logging.info('printing statistics')
        print('*'*80)
        stats_outfile.write(f"Summary Stats:\n")
        stats_outfile.write(f"Between 2003 and 2018 there were {total_cases} animal cases of rabies in China.\n")
        stats_outfile.write(f"{max_year} had the highest number of cases with {max_value}.\n")
        stats_outfile.write(f"{min_year} had the lowest number of cases with {min_value}.\n")

        stats_outfile.write(f"Average number of cases per year was {avg_year}%.\n")

        stats_outfile.write(f"Mumber of unique viral clades was {unique_clades}.\n")
        stats_outfile.write(f"Most common clade was {max_clade}, identified {max_value} times.\n")
        stats_outfile.write(f"Rarest clade was {min_clade}, reported {min_value} times.\n")


def print_data(outfile, args):
    '''prints data to either csv file or terminal of the comprehensive list of clean data'''
    logging.info('printing data')
    rdata = AnimalRABVData()
    columns = ['location','animal species', 'year', 'clade']
    writer = csv.writer(outfile)
    writer.writerow(columns)
    for line in rdata:
        writer.writerow(line)


def figure_maker():
    rdata = AnimalRABVData()
    logging.debug('making figure')
    plt.set_loglevel("info")
    plt.figure(1)
    plt.suptitle('Animal Rabies Cases in China; 2003 - 2018', fontweight='bold')

    #graph 1: number of cases per year
    x_yr, y_dom, y_wild = rdata.sep_wild_dom()
    y_dom_np = np.array(y_dom)
    y_wild_np =np.array(y_wild)
    plt.subplot(2, 2, 1)
    plt.bar(x_yr, y_dom_np, color='darkmagenta', label="Domestic")
    plt.bar(x_yr, y_wild_np, bottom=y_dom_np, color='orchid', label="Wild")
    plt.title('Domestic vs Wild Cases Per Year')
    plt.legend(loc='upper right', bbox_to_anchor=(0.3, 1))
    plt.xticks(rotation=45)
    plt.xlabel('Year')
    plt.ylabel('Number of Cases')
    #end graph 1

    #graph 2: bar graph of clades
    years, clades = rdata.data_structures()
    x_clade, y_clade = clades
    plt.subplot(2,2,2)
    plt.bar(x_clade, y_clade)
    plt.title('Distribution of Unique Viral Clades')
    plt.xticks(rotation=90)
    plt.xlabel('Clade')
    plt.ylabel('Count')
    plt.subplots_adjust(hspace=0.8, wspace=0.3)
    logging.info('returning figure')
    #end graph 2

    #graph 3: pie chart of animal species
    plt.subplot(2, 2, 3)
    plt.rcParams["figure.autolayout"] = True
    labels = [k for k in rdata.animal_counts()]
    sizes = [float(v) for v in rdata.animal_counts().values()]
    pie = plt.pie(sizes, autopct=('%.1f%%'), shadow=True, startangle=90, radius=2, pctdistance=1.1)
    plt.title('Animal Species Distribution')
    plt.subplot(2, 2, 4)
    plt.legend(pie[0], labels, bbox_to_anchor=(.1,1), title="Animal Species")
    plt.axis('off')
    #end graph 3

    return plt.show()


def get_args(arg_source):
    parser = argparse.ArgumentParser(description='analyze animal rabies data')

    parser.add_argument('command', metavar='<command>', choices=['print'], help='command to execute')

    parser.add_argument('-o', '--ofile', dest='outfile', action='store', metavar='<outfile>',help='File to which output should be written' )

    parser.add_argument('-s', '--stats', dest='stats', action='store', metavar='<stats_outfile>', help='File to which stats summary should be written' )

    parser.add_argument('-p', '--plot', dest='plot', action='store_true', default=False)

    return parser.parse_args(arg_source)


def main():
    from logger import set_up_log
    set_up_log('animal_log.log')
    rdata = AnimalRABVData()

    args = get_args(sys.argv[1:])

    if args.outfile is None:
        for line in rdata:
            print(f'Rabies cases, China:({line[0]}, {line[1]}, {line[2]}, {line[3]})')
    
    else:
        with open(args.outfile, 'w') as outfile:
            #need header
            print_data(outfile, args)

    if args.stats is None:
        rdata.general_stats(sys.stdout, args)

    else: 
        with open(args.stats, 'w') as stats_outfile:
            rdata.general_stats(stats_outfile, args)
        logging.info(f"stats summary printed to {outfile}")
        logging.info(f"closing {outfile}")

    if args.plot:
        figure_maker()
        logging.info('figure printed')

    rdata.sep_wild_dom()


if __name__ == '__main__':
    main()