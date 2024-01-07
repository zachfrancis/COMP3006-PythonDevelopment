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


class TieGame(Exception):
    pass


class Hand:
    """Class that encapsulates a Blackjack hand."""

    def __init__(self, cards = None):
        self.cards = cards if cards else []
        self.total = 0
        self.soft_ace_count = 0
        self.score()

    def __str__(self):
        return f"Hand of {self.cards}, with score {self.total}, and {self.soft_ace_count} soft aces."

    def add_card(self):
        """Add a random card to the Hand."""
        self.cards.append(get_card())
        self.score()

    def is_blackjack(self):
        """Return True if the cards in Hand are a Blackjack"""
        return (self.total == 21 and len(self.cards) == 2)

    def is_bust(self):
        """Return True if the Hand is a bust."""
        return self.total > 21

    def score(self):
        """Calculate the score of a Blackjack hand."""

        # Change all cards above 10 to equal 10
        cards = [card if card < 11 else 10 for card in self.cards]
        total, soft_ace_count = (0, 0)
        
        # Assume all aces are 11 and keep a count of the aces
        for card in cards:
            if card == 1:
                total += 11
                soft_ace_count += 1
            else:
                total += card

        # If score is above 21 and aces are present, subtract from the score
        # until there are no more aces or the score is under twenty one
        while (soft_ace_count > 0 and total > 21):
            total -= 10
            soft_ace_count -= 1

        self.total = total
        self.soft_ace_count = soft_ace_count
        return Score(total, soft_ace_count)

class Strategy:
    def __init__(self, stand_on_value, stand_on_soft):
        self.stand_on_value = stand_on_value
        self.stand_on_soft = stand_on_soft

    def __repr__(self):
        return f"Strategy(stand_on_value={self.stand_on_value}, stand_on_soft={self.stand_on_soft})"

    def __str__(self):
        _str = 'S' if self.stand_on_soft else 'H'
        _str += str(self.stand_on_value)
        return _str

    def stand(self, hand):
        """Determine whether to stand on a given Hand."""
        assert(isinstance(hand, Hand))
        total, soft_aces = hand.score()

        if (total < self.stand_on_value):
            return False

        if (total == self.stand_on_value and soft_aces and not self.stand_on_soft):
            return False

        return True

    def play(self):
        """Play through a hand of Blackjack until it stands or busts."""
        # Hands start with 2 cards
        hand = Hand(cards=[get_card(), get_card()])

        # Continue to deal cards until stand condition is reached
        while not self.stand(hand):
            hand.add_card()

        return hand


def parseStrategy(strategy):
    """Return stand on soft on stand value from a Blackjack strategy
    
    Strategy should be a string starting with 'H' or 'S' and ending in an 
    integer between 13 and 20"""
    stand_on_soft = True if strategy[0] == 'S' else False
    stand_value = int(strategy[1:])
    return (stand_value, stand_on_soft)


def simulateBlackjackGame(playerStrategy, dealerStrategy):
    """Simulate a hand of Blackjack
    
    Return True if player wins, False otherwise"""
    pSoftVal, pSoftStand = parseStrategy(playerStrategy)
    player = Strategy(pSoftVal, pSoftStand)
    pHand = player.play()

    # End game if the player busts
    if pHand.is_bust():
        return False

    dSoftVal, dSoftStand = parseStrategy(dealerStrategy)
    dealer = Strategy(dSoftVal, dSoftStand)
    dHand = dealer.play()

    # End game if dealer busts
    if dHand.is_bust():
        return True

    # Check all win/loss conditions
    if pHand.is_blackjack() and not dHand.is_blackjack():
        return True
    if dHand.is_blackjack() and not pHand.is_blackjack():
        return False
    if pHand.total == dHand.total:
        raise TieGame # SPecial case where the run is thrown out
    if pHand.total > dHand.total:
        return True
    return False
    

def build_table(num_runs, strategy_list):
    writer = csv.writer(sys.stdout)
    writer.writerow(['P-Strategy'] + ['D-' + strat for strat in strategy_list])

    # Iterate through strategy table for the player, then for the dealer
    for playerStrategy in strategy_list:
        row = ['P-' + playerStrategy]   # Row title
        for dealerStrategy in strategy_list:
            winCount = 0
            countedRuns = num_runs
            for run in range(num_runs):
                try:
                    if simulateBlackjackGame(playerStrategy, dealerStrategy):
                        winCount += 1
                except TieGame:
                    countedRuns -= 1
            row.append(f"{winCount / num_runs * 100:.2f}")
        writer.writerow(row)


def makeStrategyList(lower_limit, upper_limit):
    """Makes list of Blackjack strategies as strings"""
    strategy_list = []
    for hold_val in range(lower_limit, upper_limit + 1):
        for strat in ['H','S']:
            strategy_list.append(strat + str(hold_val))
    return strategy_list


def main():
    # Input validation
    if (len(sys.argv) != 2):
        print("Please provide 1 argument: number of simulations to run")
        sys.exit(1)
    num_runs = int(sys.argv[1])

    # Make a strategy list and build the simulation table
    strategy_list = makeStrategyList(13, 20)
    build_table(num_runs, strategy_list)


if __name__ == '__main__':
    main()