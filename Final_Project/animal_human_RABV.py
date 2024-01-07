#!/usr/bin/env python3

import logging
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import numpy as np
import csv


from rabv_animal import AnimalRABVData
from rabies_analysis import RabiesAnalyzer as HumanRABVData


class MergeRABVData:
    '''structures animal data to merge with human data'''
    def __init__(self):
        '''initializes a list of animal data generated from rabv_animal module'''
        logging.debug('accessing data from rabv_animal')
        aRABV = AnimalRABVData()
        self.adata = aRABV.data


    def dict_structure(self, animal):
        '''dictionary constructor that passes in an animal type and counts the number of times that animal appears in a datalist for each year. Returns a dictionary with the key as the year and count as the value for that animal'''
        logging.debug('counting species per year')
        animalDict = defaultdict(int)
        for x in range(2003,2012):
            animalDict[x]

        for line in self.adata:
            for key in animalDict:
                if line[2] == key and line[1] == animal:
                    animalDict[key] += 1
        return animalDict

    def animal_dict(self):
        '''creates a list of dictionaries where the key is the animal species and the value is a dictionary with the counts per year generated from dict_structure module'''
        logging.debug('creating list of animal dictionaries')
        animals = ['Dog', 'Cattle', 'Pig', 'Sheep', 'Camel', 'Fox', 'Raccoon dog', 'Deer', 'Ferret badger']
        animal_dict = {}
        animal_list_dict = []
        for animal in animals:
            animal_dict[animal] = self.dict_structure(animal)
        animal_list_dict.append(animal_dict)
        return animal_list_dict

    def location(self):
        logging.debug('counting number of animal cases by location')
        #tallying number of animal deaths by location
        with open('rabv_animal.csv', 'r') as f:
            reader = csv.reader(f)
            location_list = []
            for row in reader:
                location_list.append(row[0].replace('*','').strip())
        animal_dict = Counter(location_list)
        return animal_dict


def make_figure():
    mRABV = MergeRABVData()
    hRABV = HumanRABVData()
    aRABV = AnimalRABVData()

    plt.figure(1)
    plt.suptitle('Comparing Human to Animal Rabies Cases in China, 2003-2010', fontweight='bold')

    # First plot: Yearly animal cases and human exposures
    human_dict = defaultdict(int)
    animal_dict = defaultdict(int)
    
    for dat in hRABV:
        if dat.country == 'China':
            human_dict[dat.year] += dat.exposures

    for dat in aRABV.data:
        animal_dict[dat[2]] += 1

    # Create the plot
    x = np.arange(2003, 2011, 1)
    y1 = []
    y2 = []
    for year in x:
        y1.append(human_dict[year])
        y2.append(animal_dict[year])

    ax1 = plt.subplot(2, 2, 1)
    ax1.set_title('Animal Rabies Cases vs Human Exposures of Rabies in China')
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Human Exposures', color='cornflowerblue')
    ax1.plot(x, y1, color='cornflowerblue')
    ax1.tick_params(axis='y', labelcolor='cornflowerblue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Animal Cases', color='darkorange')
    ax2.plot(x, y2, color='darkorange')
    ax2.tick_params(axis='y', labelcolor='darkorange')
    # End first plot

    # Second plot: cases broken out by species by year, including humans, in China
    for row in mRABV.animal_dict():
        for (key, value) in row.items():
            if key == 'Dog':
                x = list(value.keys())
                y_dog = list(value.values())
            if key == 'Cattle':
                y_cow = list(value.values())
            if key == 'Pig':
                y_pig = list(value.values())
            if key == 'Sheep':
                y_sheep = list(value.values())
            if key == 'Camel':
                y_camel = list(value.values())
            if key == 'Fox':
                y_fox = list(value.values())
            if key == 'Raccoon dog':
                y_raccoon = list(value.values())
            if key == 'Deer':
                y_deer = list(value.values())
            if key == 'Ferret badger':
                y_ferret = list(value.values())
       
    human_dict.clear()
    for dat in hRABV:
        if dat.country == 'China':
            human_dict[dat.year] += dat.deaths
    
    y_human = [human_dict[year] for year in x]

    plt.subplot(2,2,2)
    plt.plot(x, y_dog, 'darkorange', label='Dog')
    plt.plot(x, y_cow, 'limegreen', label='Cow')
    plt.plot(x, y_pig, 'cornflowerblue', label='Pig')
    plt.plot(x, y_sheep, 'darkgray', label='Sheep')    
    plt.plot(x, y_camel, 'lightseagreen', label='Camel')
    plt.plot(x, y_raccoon, 'blueviolet', label='Raccoon dog')
    plt.plot(x, y_deer, 'darkred', label='Deer')
    plt.plot(x, y_ferret, 'hotpink', label='Ferret badger')
    plt.ylabel('Number of Cases') 
    plt.legend(title="Animal Species", loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)
    plt.twinx()
    plt.plot(x, y_human, color='#3A3A3A', alpha=0.75, label='Deaths', linewidth=3)
    plt.legend()
    plt.title('Total Cases Per Species Per Year in China')
    plt.xlabel('Year')
    plt.ylabel('Human Deaths')
    # End second plot

    # Third plot: animal cases and human deaths by country
    animal_dict = mRABV.location()

    human_dict = defaultdict(int)
    for dat in hRABV:
        if dat.country == 'Russian Federation':
            dat.country = 'Russia'
        human_dict[dat.country] += dat.deaths

    # Determine what countries are common between the dictionaries
    animal_set = set(animal_dict.keys())
    human_set = set(human_dict.keys())
    countries = animal_set.intersection(human_set)

    # These bars are so tall, they mask the other countries
    # Removing them to make the chart a bit more readable
    countries.remove('India')
    countries.remove('China')

    animal_cases = []
    human_deaths = []
    for country in countries:
        animal_cases.append(animal_dict[country])
        human_deaths.append(human_dict[country])

    plt.subplot(2,2,3)
    x = np.arange(len(countries))
    width = 0.35

    h = plt.bar(x - width/2, animal_cases, width, label='Animal', color='cornflowerblue')
    plt.ylabel('Animal Cases')
    plt.xticks(x, list(countries), rotation=90)
    plt.twinx()
    a = plt.bar(x + width/2, human_deaths, width, label='Human', color='darkorange')
    plt.title('Animal Cases and Human Deaths by Country Outside of China')
    plt.ylabel('Human Deaths')
    plt.legend([h, a], [h.get_label(), a.get_label()])
    # End third plot

    plt.subplots_adjust(hspace=0.8, wspace=0.3)
    plt.show()
     

def main():
    from logger import set_up_log
    set_up_log('animal_human.log')
    make_figure()


if __name__ == '__main__':
    main()