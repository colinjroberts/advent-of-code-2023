from tools import (get_csv_line_input_as_list, get_line_input_as_list) 
import functools 
from collections import Counter

# Constants used for ordering. I really should have made a Card class that 
# handles ordering like the other classes, but here we are, 2 days behind now!
CARD_ORDERING = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
CARD_ORDERING_JOKERS = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'] 
CARD_TYPES = ['high card', 'one pair', 'two pair', 'three of a kind', 'full house', 'four of a kind', 'five of a kind']

class Game:
    # All the logic for ordering and jokering is in the Hand class.
    # The Hand class implements ordering such that I can make a list
    # of Hands here, then sort them and the objects should all be in
    # the right order. 
    def __init__(self, list_of_hand_point_tuples, jokers=False):
        self.ordered_hands = sorted([Hand(line, jokers) for line in list_of_hand_point_tuples])

    # This calculates the answer to the problem doing the summing 
    # because the hand will already be in order from the sorting above
    def total_winnings(self):
        total_winnings = 0
        for i, hand in enumerate(self.ordered_hands):
            total_winnings += hand.bid * (i + 1)
        return total_winnings

    # Pretty printing
    def __str__(self):
        return '\n'.join([str(hand) for hand in self.ordered_hands])
   
    # Pretty printing
    def __repr__(self):
        return str(self)


# The Hand class has nearly all of the logic buried in it
# - hand_type() figures out what kind of hand something is
# - __eq__ and __lt__ implement sorting based on hand type and card values
# - modified_joker_cards() takes the original cards and finds the best 
#   hand you can make with it (part 2)
# - The "@functools.total_ordering" decorator implements all comparison 
#   and equality operators I need for sorting as long as I define == and <
@functools.total_ordering
class Hand:
    def __init__(self, tuple_of_hand_and_points, jokers=False):
        
        # The string representation given by the input
        # e.g. 'AK9JQ'
        self.card_str = tuple_of_hand_and_points[0]
        # The int given by the input used for scoring
        self.bid = tuple_of_hand_and_points[1]
    
        # This is for part 1
        self.card_type = self.hand_type(self.card_str)

        # This is for part 2
        self.jokers = jokers
        self.joker_hand = self.modified_joker_cards()
        self.joker_hand_type = self.hand_type(self.joker_hand)

    # Pretty printing
    def __str__(self):
        if self.jokers:
            return f'cards: {self.card_str} jokercards: {self.joker_hand} bid: {self.bid}, hand_type: {self.joker_hand_type}'
        else:
            return f'cards: {self.card_str} bid: {self.bid}, hand_type: {self.card_type}'

    # Pretty printing
    def __repr__(self):
        return str(self)
    
    # Defines what makes two Hands equal
    # (two hands are equal if their string given by the input are equal)
    # I'm pretty sure the problem said there would be no duplicates
    def __eq__(self, other):
        return (self.card_str == other.card_str)

    # Defines what makes one Hand (self) less than (an)other
    # Implementing sorting means I can just make a list of Hands then call .sort()
    # on it or use sorted(). This logic needed to be split for jokers and non-jokers
    # because of the different values Jokers have when comparing card by card for
    # Hands of the same type.
    def __lt__(self, other):
        """
        Hands are primarily ordered based on type; for example, every full house is
        stronger than any three of a kind.
        If two hands have the same card_type, a second ordering rule takes effect. 
        Start by comparing the first card in each hand. If these cards are different,
        the hand with the stronger first card is considered stronger. If the first card
        in each hand have the same label, however, then move on to considering the 
        second card in each hand. If they differ, the hand with the higher second 
        card wins; otherwise, continue with the third card in each hand, then the
        fourth, then the fifth.
        """
        # If we are using jokers (part 2), we need to do our scoring with the special Joker
        # ordering in which Jokers are the lowest card
        if self.jokers:
            if self.joker_hand_type == other.joker_hand_type:
                # Hands have the same type, so we need to go card by card looking for which
                # individual card is lower using the special joker card ordering constant
                for self_card, other_card in zip(self.card_str, other.card_str):
                    if CARD_ORDERING_JOKERS.index(self_card) == CARD_ORDERING_JOKERS.index(other_card):
                        continue
                    else:
                        return CARD_ORDERING_JOKERS.index(self_card) < CARD_ORDERING_JOKERS.index(other_card) 
                return False
            
            else:
                # Hands are of different type, so that's our ordering!
                return CARD_TYPES.index(self.joker_hand_type) < CARD_TYPES.index(other.joker_hand_type)
        
        # If we do not have jokers (part 1), then we use the normal card ordering
        else:
            # Hands have the same type, so we need to go card by card looking for which
            # individual card is lower using the card ordering constant
            if self.card_type == other.card_type:
                # First card in each hand, stronger hard wins, keep going
                for self_card, other_card in zip(self.card_str, other.card_str):
                    if CARD_ORDERING.index(self_card) == CARD_ORDERING.index(other_card):
                        continue
                    else:
                        return CARD_ORDERING.index(self_card) < CARD_ORDERING.index(other_card) 
                return False
            
            else:
                # Hands are of different type, so that's our ordering!
                return CARD_TYPES.index(self.card_type) < CARD_TYPES.index(other.card_type)
            
    
    # All of the logic needed to find the best hand given jokers
    # The idea here is that for each number of jokers, there is a calculable 
    # best hand given what the other cards are. Also note that I when I wrote 
    # this, I didn't fully realize that I just needed to make the best hand 
    # TYPE. I was under the impression that I did actually want to make the 
    # best hand possible including card values 

    # 5 jokers - best option is to make them all 'A'
    # 4 jokers - means there is 1 non-J, turn all the J's into that one for 5 of a kind.
    # 3 jokers - means there will be 2 other cards. 
    #   - 2 (the 2 cards are the same): make the jokers match for 5 of a kind
    #   - 1, 1 (the 2 cards are different): pick the higher hard for 4 of a kind
    # 2 jokers - means there are 3 other cards
    #   - 3 (the 3 cards are the same): make the jokers match for 5 of a kind
    #   - 2, 1: match the most common (2) for a 4 of a kind
    #   - 1, 1, 1 (all different): match the highest card for 3 of a kind
    # 1 joker - 4 other cards
    #   - 4 (the same): make the jokers match 5 of a kind
    #   - 3, 1: match most common (3) for 4 of a kind
    #   - 2, 2: match the higher one for full house - didn't actually do the higher one!
    #   - 1, 1, 1, 1 (all diff): match highest for a pair
    # This code will be similar in structure to hand type below except worse
    # So much repeated code, but I'm behind! Make it work, then good, then fast
    def modified_joker_cards(self) -> str:
        # save a copy for reasons I don't remember, probably sorting related
        cards = self.card_str
        
        # no jokers, don't need to make a new better hand
        if 'J' not in cards:
            return cards
        
        # I did some sorting back when I wanted to try to make the best hand possible, 
        # but REALLY it was used for grouping numbers together. Later I worked around that
        sorted_cards_list = sorted(list(cards), key=lambda x: CARD_ORDERING_JOKERS.index(x))
        
        # Get all the cards with jokers removed
        cards_no_jokers = [c for c in sorted_cards_list if c != 'J']
        # Get the unique values of those cards.
        uniqe_cards_no_jokers = list(set(cards_no_jokers))
        
        
        # All cards are jokers, return best hand
        if len(cards_no_jokers) == 0:
            return 'AAAAA'
        
        # All but one cards is a joker
        # Match the other card for 5 of a kind
        if len(cards_no_jokers) == 1:
            return uniqe_cards_no_jokers.pop() * 5

        # There are 3 jokers and 2 non-jokers
        if len(cards_no_jokers) == 2:
            # if the non-joker cards are the same, make the jokers match for 5 of a kind
            if len(uniqe_cards_no_jokers) == 1:
                return uniqe_cards_no_jokers.pop() * 5
            
            # if the cards are different, pick the higher card for 4 of a kind
            # But need to maintain the original order, so iterate over the original
            # card order replacing the J with the better card
            else:
                higher_card = sorted(uniqe_cards_no_jokers, key=lambda x: CARD_ORDERING_JOKERS.index(x))[1]
                replaced_cards = [higher_card if c == 'J' else c for c in cards]
                return ''.join(replaced_cards)
        
        # There are 2 jokers, there are 3 non-jokers
        if len(cards_no_jokers) == 3:
            # if the cards are the same, make the jokers match for 5 of a kind
            if len(uniqe_cards_no_jokers) == 1:
                return uniqe_cards_no_jokers.pop() * 5
            
            # if there are 2 unique cards, it means we can make 4 of a kind
            # But need to maintain the original order, so iterate over the original
            # card order replacing the J with the better card
            if len(uniqe_cards_no_jokers) == 2:
                more_common_card = Counter(cards_no_jokers).most_common()[0][0]
                replaced_cards = [more_common_card if c == 'J' else c for c in cards]
                return ''.join(replaced_cards)

            # there are 3 unique cards then the best hand is a 3 of a kind with the
            # highest card
            # But need to maintain the original order, so iterate over the original
            # card order replacing the J with the better card
            if len(uniqe_cards_no_jokers) == 3:
                higher_card = sorted(uniqe_cards_no_jokers, key=lambda x: CARD_ORDERING_JOKERS.index(x))[2]
                replaced_cards = [higher_card if c == 'J' else c for c in cards]
                return ''.join(replaced_cards)

        # There is 1 joker, there are 4 non-jokers
        if len(cards_no_jokers) == 4:

            # if the cards are the same, make the jokers match for 5 of a kind
            if len(uniqe_cards_no_jokers) == 1:
                return uniqe_cards_no_jokers.pop() * 5
            
            # if there are 2 unique cards, it means there is either 2,2 or 3,1
            # T555J
            # TT55J
            # Because I don't actually need to make the Hand (only the type matters),
            # I will just grab the most common. This solves the 3,1 case and it doesn't
            # matter which one I take in the 2, 2 case. I don't need the BEST full house
            # I just need any full house.
            # As with the others, replace 'J' from oroginal card str with correct card
            if len(uniqe_cards_no_jokers) == 2:
                # But if I WERE to try to make the best full house, I'd be using this
                # higher_card = sorted(uniqe_cards_no_jokers, key=lambda x: CARD_ORDERING_JOKERS.index(x))[1]
                # replaced_cards = [higher_card if c == 'J' else c for c in cards]
                more_common_card = Counter(cards_no_jokers).most_common()[0][0]
                replaced_cards = [more_common_card if c == 'J' else c for c in cards]
                return ''.join(replaced_cards)

            # there are 3 unique cards which means one of them shows up twice.
            # We can either make 2 pair or 3 of a kind. 3 of a kind is bigger
            # As with the others, replace 'J' from oroginal card str with correct card
            if len(uniqe_cards_no_jokers) == 3:
                more_common_card = Counter(cards_no_jokers).most_common()[0][0]
                replaced_cards = [more_common_card if c == 'J' else c for c in cards]
                return ''.join(replaced_cards)        
            
            # there are 4 unique cards then the best hand is a pair with the highest card
            # As with the others, replace 'J' from oroginal card str with correct card
            if len(uniqe_cards_no_jokers) == 4:
                higher_card = sorted(uniqe_cards_no_jokers, key=lambda x: CARD_ORDERING_JOKERS.index(x))[3]
                replaced_cards = [higher_card if c == 'J' else c for c in cards]
                return ''.join(replaced_cards)  
        
        # Raise an error in case this terrible if else logic doesn't work
        raise ValueError("No jokers!?!?!?")


    # Determines the type of this Hand's cards
    def hand_type(self, card_string) -> str:
        cards = sorted(list(card_string))
        uniqe_cards = list(set(cards))
        
        # Five of a kind, where all five cards have the same label: AAAAA
        if len(uniqe_cards) == 1:
            return CARD_TYPES[6]
        
        if len(uniqe_cards) == 2:
            # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
            # If the most common card appears 4 times
            if Counter(cards).most_common()[0][1] == 4:
                return CARD_TYPES[5]

            # Otherwise, it MUST be 2, 3/Full house, where three cards have the same label, and 
            # the remaining two cards share a different label: 23332
            else:
                return CARD_TYPES[4]
        
        if len(uniqe_cards) == 3:
            # Three of a kind, where three cards have the same label, and the remaining 
            # two cards are each different from any other card in the hand: TTT98
            if Counter(cards).most_common()[0][1] == 3:
                return CARD_TYPES[3]

            # Two pair, where two cards share one label, two other cards share a second label, 
            # and the remaining card has a third label: 23432
            else:
                return CARD_TYPES[2]

        # High card, where all cards' labels are distinct: 23456
        if len(uniqe_cards) == 5:
            return CARD_TYPES[0]

        # One pair, where two cards share one label, and the other three cards have a 
        # different label from the pair and each other: A23A4
        return CARD_TYPES[1]
                


def part1(input_list):
    # All of the logic for evaluating and sorting hands of cards,
    # which is the real meat of the problem, happens in the Hand class.
    # This line is some list comprehension nonsense that iterates of each 
    # line in the input, splits the line, and saves the string of card
    # values and an int with the bid amount. The result is a list of tuples
    # [('AAAAA', 141), ('KQQQQ', 5), ...]
    card_bid_tuples = [(card_str, int(num_str)) for card_str, num_str in [item.split(' ') for item in input_list]]
    
    # All of the logic is encapsulated in this Game class and the Hand class
    # the total_winnings() method calculates the score
    game = Game(card_bid_tuples)
    # print(game)
    
    # I'm going to leave these here for playing with 
    # h1 = Hand(('KQQQQ', 5))
    # h2 = Hand(('KK9KK', 5))
    # print(h1)
    # print(h2)
    # print(h1 < h2)
    return game.total_winnings()


# Possibilities:
# - Make all hand combinations basically nested loops for each joker
#   saving the highest hand.
# - There are probably fixed options. Like if it is all jokers, there's 
#   only 1 best option. If there are 4 jokers, it's  the same, the best
#   option is to copy the 1 non joker for 5 of a kind. Let's run with that!
def part2(input_list):
    # Same as above. List comprehension resulting in a list of tuples
    # [('AAAAA', 141), ('KQQQQ', 5), ...]
    card_bid_tuples = [(card_str, int(num_str)) for card_str, num_str in [item.split(' ') for item in input_list]]
    
    # Same as above, but now with a second argument for the jokers field! 
    game = Game(card_bid_tuples, True)
    # print(game)

    return game.total_winnings()
    


def p07():
    test_filename1 = "inputs/07-test1.txt"
    test_filename2 = "inputs/07-test2.txt"
    filename = "inputs/07.txt"

    input_list_test1 = get_line_input_as_list(test_filename1, "string")
    input_list_test2 = get_line_input_as_list(test_filename2, "string")
    input_list = get_line_input_as_list(filename, "string")

    test_output1 = part1(input_list_test1)
    test_output2 = part2(input_list_test2)

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1, output2
    return None, test_output2
    return test_output1, test_output2
    return test_output1, None
    return output1, None
