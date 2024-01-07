#!/usr/bin/env python3

import argparse
import sys
import csv
import logging
import matplotlib.pyplot as plt
import numpy as np

from collections import defaultdict
from itertools import islice


class RabiesInfo:
    """Class that holds relevant rabies data"""
    def __init__(self, cont, country, pep, pop, deaths, exposures, year):
        self.continent = str(cont)
        self.country  = str(country)
        self.pep = True if pep == 'Y' else False # Post-Exposure Prophylaxis (preventative treatment)
        self.population = int(pop)
        self.deaths = int(deaths)
        self.exposures = int(exposures)
        self.year = int(year)

    def __repr__(self):
        return f"RabiesInfo({self.country}, {self.year}, {self.population}, {self.deaths}, {self.exposures}, PEP: {self.pep})"

    def __str__(self):
        return self.__repr__()
        
    def __eq__(self, other):
        if type(self) == type(other):
            return (self.continent, self.country, self.year, self.population, self.deaths, self.exposures, self.pep) == \
                (other.continent, other.country, other.year, other.population, other.deaths, other.exposures, other.pep)
        return NotImplemented

    def __lt__(self, other):
        if type(self) == type(other):
            return (self.continent, self.country, self.year, self.population, self.deaths, self.exposures, self.pep) < \
                (other.continent, other.country, other.year, other.population, other.deaths, other.exposures, self.pep)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.continent, self.country, self.year, self.population, self.deaths, self.exposures, self.pep)


class RabiesAnalyzer:
    """Class the reads and performs operations on rabies data"""
    DATA_FILE = "rabies_epidemic_data.csv"
    FIELDNAMES = ['Continent', 'Country', 'Population', 'Deaths', 'Exposures', 'Year', 'PEP']

    def __init__(self):
        """Rabies data is opened on initialization"""
        logging.info("Initializing a rabies analyzer object")
        self.open_data()

    def __iter__(self):
        return iter(self.data)

    def open_data(self):
        """Opens data file and passes to parse function"""   
        with open(self.DATA_FILE, 'r') as f:
            self.data = self.parse_data(f)

    def clean_header(self, row):
        """Helper function to clean up spaces and slashes in the header names"""
        for i, col in enumerate(row):
            row[i] = col.replace('/', '_per_').replace(' ','')

    def parse_data(self, f):
        """Creates RabiesInfo object for each line in f"""
        reader = csv.DictReader(f)

        # Clean up the header names by removing spaces and slashes
        for i, col in enumerate(reader.fieldnames):
            reader.fieldnames[i] = col.replace('/', '_per_').replace(' ','')

        data = []
        count = 0
        lineno = 1
        for row in reader:
            lineno += 1

            # Pull out relevant fields and make any needed corrections
            cont = row['Continent']
            country = row['Country']
            pep = row['PP']
            pop = row['country_population'].replace(',','')
            deaths = row['Deaths_per_yr']
            exposures = row['Exposures_per_yr']

            # If there is no entry, just assume 0
            if not deaths:
                deaths = 0
            if not exposures:
                exposures = 0

            # Some of the dates have ranges like 2008-2010. 
            try:
                years = row['Year'].split('-') 
                if len(years) > 1:
                    # Going to just create a data object for each year
                    years = range(int(years[0]), int(years[-1]) + 1)
                else:
                    years = [int(years[0])]
            except ValueError:
                logging.warning(f"Invalid year in data for {country} on line {lineno}")
                continue
            
            for year in years:
                # If the years are a range, assume the data is the same for each year in the range
                data.append(RabiesInfo(cont, country, pep, pop, deaths, exposures, year))
                count += 1

        logging.info(f"Processed {lineno - 1} lines and created {count} RabiesInfo objects")
        return sorted(data)

    def sort_by_year(self):
        logging.info("Sorting rabies data by year")
        list.sort(self.data, key=lambda ri : (ri.year, ri.continent, ri.country))

    def sort_by_country(self):
        logging.info("Sorting rabies data by country")
        list.sort(self.data, key=lambda ri : (ri.country, ri.continent, ri.year))
                
def dump_data(analyzer): 
    """Write all rabies data to csv file"""
    with open('rabies_info_dump.csv', 'w') as f:
        logging.info("Dumping all rabies data to rabies_info_dump.csv")
        writer = csv.writer(f)
        writer.writerow(analyzer.FIELDNAMES)
        for dat in analyzer:
            writer.writerow([dat.continent, dat.country, dat.population, 
                                dat.deaths, dat.exposures, dat.year, dat.pep])


def list_countries(analyzer):
    """List unique countries in the data set"""
    logging.debug("Creating a list of available countries")
    countries = set()
    for dat in analyzer:
        countries.add(dat.country)
    print("Countries included in the rabies data set:")
    for country in sorted(countries):
        print(country)


def plot_countries(analyzer):
    """Plot death rate by country"""
    logging.info("Generating a plot of death rate per country")
    analyzer.sort_by_country()
    country_dict = defaultdict(lambda: [0, 0])
    for dat in analyzer:
        country_dict[dat.country][0] += dat.deaths
        country_dict[dat.country][1] += dat.population

    # Divide the total deaths by the population to normalize the data
    for country in country_dict.keys():
        avg_death_rate = (country_dict[country][0] / country_dict[country][1]) 
        country_dict[country] = avg_death_rate

    # Sort the dictionary by death rate
    country_dict = dict(sorted(country_dict.items(), key=lambda item: item[1], reverse=True))

    # Output data to a csv
    with open('death_rate_by_country.csv', 'w') as f:
        logging.info("Outputting data to death_rate_by_country.csv")
        writer = csv.writer(f)
        writer.writerow(['Country', 'Death Rate'])
        for country in country_dict:
            writer.writerow([country, f"{country_dict[country]:.2e}"])

    # Pull out the top 15 countries for the plot
    country_dict = dict(islice(country_dict.items(), 15))

    # Create the plot
    fig, ax = plt.subplots()
    ax.bar(country_dict.keys(), country_dict.values())
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
    ax.set_title("Top Yearly Death Rate for Rabies")
    ax.set_ylabel("Yearly Death Rate")
    fig.subplots_adjust(bottom=0.2)
    plt.show()


def plot_years(analyzer):
    """Plot the yearly data

    This plot isn't at all useful since the data is not at all standardized by year. There is
    at least a continuous amount of data between the years 2004-2011."""
    logging.info("Generating a plot of yearly death and exposure rates")
    analyzer.sort_by_year()
    death_dict = defaultdict(list)
    exp_dict = defaultdict(list)

    for dat in analyzer:
        death_dict[dat.year].append(dat.deaths)
        exp_dict[dat.year].append(dat.exposures)

    # 2004 - 2010 seems to have the best data
    x = np.arange(2004, 2011, 1)

    # Calculate the average deaths and exposures per year since there is a disparity
    # in the quantity of data for each year
    avg_deaths = []  
    avg_exps = []
    for year in x:
        deaths = np.array(death_dict[year])
        avg_deaths.append(deaths.mean())
        exps = np.array(exp_dict[year])
        avg_exps.append(exps.mean())

    # Output data to a csv
    with open('yearly_rates.csv', 'w') as f:
        logging.info("Outputting data to yearly_rates.csv")
        writer = csv.writer(f)
        writer.writerow(['Year', 'Deaths', 'Exposures'])
        for i in range(len(x)):
            writer.writerow([x[i], f"{avg_deaths[i]:.2f}", f"{avg_exps[i]:.2f}"])

    # Create the plot
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Avg Deaths', color='blue')
    ax1.set_title('Yearly Deaths and Exposures (Averaged)')
    ax1.plot(x, avg_deaths, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Avg Exposures', color='red')
    ax2.plot(x, avg_exps, color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    fig.tight_layout()
    plt.show()


def plot_pep(analyzer):
    """Compare deaths for regions with Post-Exposure Prophylaxis (PEP) and no PEP
    
    Theoretically this should show how effective PEP programs are per continent since the 
    death rate should be lower in regions with PEP programs in place"""
    pep_dict = defaultdict(lambda: defaultdict(list))
    for dat in analyzer:
        if dat.pep:
            pep_dict[dat.continent]['PEP'].append(dat.deaths / dat.population)
        else:
            pep_dict[dat.continent]['noPEP'].append(dat.deaths /dat.population)

    # Calculate the means per continent
    continents = [cont for cont in pep_dict.keys()]
    continents.remove('Eurasia') # Not enough data in Eurasia, just delete it
    continents.remove('Oceania') # Same for Oceania
    for cont in continents:
        pep = np.array(pep_dict[cont]['PEP'])
        no_pep = np.array(pep_dict[cont]['noPEP'])
        pep_dict[cont]['PEP'] = pep.mean()
        pep_dict[cont]['noPEP'] = no_pep.mean()

    # Output data to a csv
    with open('pep_effectiveness.csv', 'w') as f:
        logging.info("Outputting data to pep_effectiveness.csv")
        writer = csv.writer(f)
        writer.writerow(['Continent', 'PEP Death Rate', 'No PEP Death Rate'])
        for cont in continents:
            writer.writerow([cont, f"{pep_dict[cont]['PEP']:.2e}", f"{pep_dict[cont]['noPEP']:.2e}"])

    # Create the plot
    x = np.arange(len(continents))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width/2, [pep_dict[cont]['PEP'] for cont in continents], width, label='PEP')
    ax.bar(x + width/2, [pep_dict[cont]['noPEP'] for cont in continents], width, label='No PEP')

    ax.set_title('Effectiveness of PEP Programs by Continent')
    ax.set_ylabel('Deaths (Normalized by Population)')
    ax.set_xticks(x, continents)
    ax.legend()

    fig.tight_layout()
    plt.show()


def process_args(args):
    """Process command line arguments"""
    analyzer = RabiesAnalyzer()

    # Print all the countries that are present in the data
    if args.list:
        list_countries(analyzer)

    # Plot options
    if args.plot == 'countries':
        plot_countries(analyzer)
    elif args.plot == 'years':
        plot_years(analyzer)
    elif args.plot == 'pep':
        plot_pep(analyzer)

    # Dumping the data last will preserve whatever sort was done on the data
    if args.dump:
        dump_data(analyzer)


def main():
    ### BEGIN LOGGING SETUP ###
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s][%(asctime)s][%(name)s] %(message)s')

    # Add handler for stdout
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # Add handler for logging to a file
    fh = logging.FileHandler(filename='rabies_analysis.log', mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ### END LOGGING SETUP ###

    parser = argparse.ArgumentParser(description="Analyze rabies data (no arguments prints this help message)")
    parser.add_argument('-d', '--dump', dest='dump', action='store_true',
                        default=False, help='Dump all rabies data to csv file')
    parser.add_argument('-l','--list', dest='list', action='store_true', 
                        default=False, help="List available countries")
    parser.add_argument('-p', '--plot', dest='plot', action='store', type=str,
                        metavar='<plot_choice>', choices=['countries', 'years', 'pep'], 
                        help="Choose a plot to display: countries, years, or pep")
    args = parser.parse_args()

    if (len(sys.argv) < 2):
        parser.print_help()
        sys.exit(1)

    process_args(args)


if __name__ == "__main__":
    main()