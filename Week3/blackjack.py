#!/usr/bin/env python3

import sys
import random


def get_card():
    """Return a card value between 1 and 13"""
    return random.randint(1, 13)


def score(cards):
    """Calculate the score of a BLackjack hand"""

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
        
    return (total, 1) if ace_count else (total, 0)


def stand(stand_on_value, stand_on_soft, cards):
    """Determine whether to stand on a given hand"""
    
    total, soft_ace_count = score(cards)
    if (total < stand_on_value):
        return False

    if (total == stand_on_value and soft_ace_count and not stand_on_soft):
        return False

    return True


def parse_inputs(args):
    usage_msg = """
    USAGE: blackjack.py <num-simulations> <stand-on-value> <strategy>

    num-simulations - number of simulations to run, INT greater than 0
    stand-on-value - score on which to stand, INT between 1 and 20
    strategy - must be 'soft' or 'hard'
    """
    if (len(args) != 4):
        print("Incorrect number of arguments provided")
        print(usage_msg)
        sys.exit(1)
    try:
        num_runs = int(args[1])
        stand_value = int(args[2])    
        strategy = args[3]
        if (num_runs < 1 or stand_value < 1 or stand_value > 20):
            raise ValueError
        if not (strategy == 'soft' or strategy == 'hard'):
            raise ValueError
    except ValueError:
        print("Invalid argument provided")
        print(usage_msg)
        sys.exit(2)

    stand_on_soft = True if strategy == 'soft' else False
    return (num_runs, stand_value, stand_on_soft)


def main():
    num_runs, stand_value, stand_on_soft = parse_inputs(sys.argv)

    num_busts = 0
    for _ in range(num_runs):
        hand = [get_card(), get_card()]
        while not stand(stand_value, stand_on_soft, hand):
            hand.append(get_card())
        if score(hand)[0] > 21:
            num_busts += 1
    bust_percentage = num_busts / num_runs
    print(bust_percentage)


if __name__ == '__main__':
    main()