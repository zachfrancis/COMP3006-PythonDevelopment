#!/usr/bin/env python3

import sys
import random
import csv
from collections import namedtuple, defaultdict

Score = namedtuple('Score', 'total soft_ace_count')
Stand = namedtuple('Stand', 'stand total')

def get_card():
    """Return a card value between 1 and 13"""
    return random.randint(1, 13)


def score(cards):
    """Calculate the score of a Blackjack hand"""

    # Change all cards above 10 to equal 10
    cards = [card if card < 11 else 10 for card in cards]
    total, ace_count = (0, 0)
    
    # Assume all aces are 11 and keep a count of the aces
    for card in cards:
        if card == 1:
            total += 11
            ace_count += 1
        else:
            total += card

    # If score is above 21 and aces are present, subtract from the score
    # until there are no more aces or the score is under twenty one
    while (ace_count > 0 and total > 21):
        total -= 10
        ace_count -= 1

    return Score(total, ace_count)


def stand(stand_on_value, stand_on_soft, cards):
    """Determine whether to stand on a given hand"""
    
    s = score(cards)
    if (s.total < stand_on_value):
        return Stand(False, s.total)

    if (s.total == stand_on_value and s.soft_ace_count and not stand_on_soft):
        return Stand(False, s.total)

    return Stand(True, s.total)


def play_hand(stand_on_value, stand_on_soft):
    """Play a Blackjack hand, return the total"""
    
    # All hands start with two cards
    hand = [get_card(), get_card()]

    # Continue to deal cards until stand condition is reached
    while True: 
        stand_returns = stand(stand_on_value, stand_on_soft, hand)
        if stand_returns.stand:
            return stand_returns.total if stand_returns.total < 22 else 22
        hand.append(get_card())


def simulate_strategy(stand_value, stand_on_soft, iterations):
    """
    Run simulation of Blackjack strategy, keeping tally of scores then 
    calculate the percentage that each score was earned
    
    return: dict of scores and their percentage earned, last entry is # of busts
    """
    score_dict = defaultdict(int)

    # Keep a tally of the final score every iteration
    for _ in range(iterations):
        score = play_hand(stand_value, stand_on_soft)
        if score < 22:
            score_dict[str(score)] += 1
        else:
            score_dict['BUST'] += 1

    # Convert the counts to percentages
    for score in score_dict.keys():
        if score != 'BUST':
            score_dict[score] = score_dict[score] / iterations * 100
            score_dict[score] = str("{:.2f}").format(score_dict[score])

    # Add strategy at the end to make the above logic easier
    score_dict['STRATEGY'] = 'S' if stand_on_soft else 'H' 
    score_dict['STRATEGY'] += str(stand_value)

    return score_dict


def main():
    if (len(sys.argv) != 2):
        print("Please provide 1 argument: number of simulations to run")
        sys.exit(1)
    num_runs = int(sys.argv[1])

    fieldnames = ['STRATEGY','13','14','15','16','17','18','19','20','21','BUST']
    writer = csv.DictWriter(sys.stdout, fieldnames, restval="{:.2f}".format(0.0))
    writer.writeheader()
    for stand_val in range(13, 21):
        writer.writerow(simulate_strategy(stand_val, False, num_runs))
        writer.writerow(simulate_strategy(stand_val, True, num_runs))


if __name__ == '__main__':
    main()