from tools import (get_csv_line_input_as_list, get_line_input_as_list) 
import functools 

CARD_ORDERING = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
CARD_ORDERING_JOKERS = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'] 
CARD_TYPES = ['high card', 'one pair', 'two pair', 'three of a kind', 'full house', 'four of a kind', 'five of a kind']

class Game:
    def __init__(self, list_of_hand_point_tuples):
        self.ordered_hands = sorted([Hand(line) for line in list_of_hand_point_tuples])

    def total_winnings(self):
        total_winnings = 0
        for i, hand in enumerate(self.ordered_hands):
            total_winnings += hand.bid * (i + 1)
        return total_winnings

    def __str__(self):
        return '\n'.join([str(hand) for hand in self.ordered_hands])

    def __repr__(self):
        return str(self)
    
@functools.total_ordering
class Card:
    def __init__(self, string_value):
        self.card_str = string_value
    
    def __str__(self):
        return self.card_str
    
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (self.card_str == other.card_str)

    def __lt__(self, other):
        return CARD_ORDERING.index(self.card_str) < CARD_ORDERING.index(other.card_str) 


@functools.total_ordering
class Hand:
    def __init__(self, tuple_of_hand_and_points, jokers=False):
        self.card_str = tuple_of_hand_and_points[0]
        self.jokers = jokers
        if jokers:
            self.card_str = self.modify_cards_with_jokers()

        self.bid = int(tuple_of_hand_and_points[1])
        self.card_type = self.hand_type()
    
    def __str__(self):
        return f'cards: {self.card_str} bid: {self.bid}, hand_type: {self.card_type}'
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return (self.card_str == other.card_str)

    def __lt__(self, other):
        """
        If two hands have the same card_type, a second ordering rule takes effect. 
        Start by comparing the first card in each hand. If these cards are different,
        the hand with the stronger first card is considered stronger. If the first card
        in each hand have the same label, however, then move on to considering the 
        second card in each hand. If they differ, the hand with the higher second 
        card wins; otherwise, continue with the third card in each hand, then the
        fourth, then the fifth.
        """
        # Absolute base to make it easier to find the max in part 2
        if self.bid == -1:
            return True
        
        # Same card_type
        if self.card_type == other.card_type:
            # First card in each hand, stronger hard wins, keep going
            for self_card, other_card in zip(self.card_str, other.card_str):
                if self.jokers:
                    if CARD_ORDERING_JOKERS.index(self_card) == CARD_ORDERING_JOKERS.index(other_card):
                        continue
                    else:
                        return CARD_ORDERING_JOKERS.index(self_card) < CARD_ORDERING_JOKERS.index(other_card) 
                    
                else:
                    if CARD_ORDERING.index(self_card) == CARD_ORDERING.index(other_card):
                        continue
                    else:
                        return CARD_ORDERING.index(self_card) < CARD_ORDERING.index(other_card) 
            return False
        
        # Different types
        else:
            if CARD_TYPES.index(self.card_type) < CARD_TYPES.index(other.card_type):
                return True
        
        return False
            
    # Takes this Hand's cards and returns the best possible hand replacing jokers 
    def modify_cards_with_jokers(self) -> str:
        # The idea here is given a hand with one or more jokers in it,
        # figure out what the best option is for the jokers. 
        # 5 jokers - best option is to make them all 'A'
        # 4 jokers - means there is 1 non-J, turn all the J's into that one for 5 of a kind.
        # 3 jokers - means there will be 2 other cards. 
        #   - if the cards are the same, make the jokers match for 5 of a kind
        #   - if the cards are different, pick the higher hard for 4 of a kind
        # 2 jokers - means there are 3 other cards
        #   - 3 cards are the same: make the same for  5 of a kind
        #   - 2, 1: match the 1 for a full house
        #   - all different: match the highest card for 3 of a kind
        # 1 joker - 4 other cards
        #   - 4 the same, match for 5 of a kind
        #   - 3, 1 match 3 for 4 of a kind
        #   - 2, 2 match the higher one for full house
        #   - all diff match highest for a pair
        # This code will be similar in structure to hand type below
        
        
        cards = self.card_str
        # Note that this sort is in alpha order. I didn't make
        # a Card class to do this sorting, but I really should
        sorted_cards_list = sorted(list(self.card_str))
        uniqe_cards = list(set(sorted_cards_list))
        
        # no jokers
        if 'J' not in uniqe_cards:
            return cards
        
        cards_no_jokers = [c for c in sorted_cards_list if c != 'J']
        uniqe_cards_no_jokers = cards_no_jokers.copy().remove('J')
        
        # All cards are jokers
        if len(cards_no_jokers) == 0:
            return 'AAAAA'
        
        # All but one cards is a joker
        # Match the other card for 5 of a kind
        if len(cards_no_jokers) == 1:
            return uniqe_cards_no_jokers.pop() * 5

        # There are 2 jokers and 3 non jokers
        if len(cards_no_jokers) == 2:
            # if the cards are the same, make the jokers match for 5 of a kind
            if len(uniqe_cards_no_jokers) == 1:
                return uniqe_cards_no_jokers.pop() * 5
            
            # if the cards are different, pick the higher hard for 4 of a kind
            else:
                higher_card = uniqe_cards_no_jokers
                return uniqe_cards_no_jokers.pop() * 5
                return 'AAAAA'
        
        if len(cards_no_jokers) == 2:
            return 'AAAAA'
        
        if len(cards_no_jokers) == 1:
            return 'AAAAA'
        
        
        raise ValueError("No jokers!?!?!?")

    # Determines the type of this Hand's cards
    def hand_type(self) -> str:
        cards = sorted(list(self.card_str))
        uniqe_cards = list(set(cards))
        
        # Five of a kind, where all five cards have the same label: AAAAA
        if len(uniqe_cards) == 1:
            return CARD_TYPES[6]
        
        if len(uniqe_cards) == 2:
            # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
            if len([c for c in cards if c == uniqe_cards[0]]) == 4 or len([c for c in cards if c == uniqe_cards[1]]) == 4:
                return CARD_TYPES[5]
            # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
            else:
                return CARD_TYPES[4]
        
        if len(uniqe_cards) == 3:
            # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
            for i in range(3):
                if len([c for c in cards if c == uniqe_cards[i]]) == 3:
                    return CARD_TYPES[3]

            # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
            else:
                return CARD_TYPES[2]

        # High card, where all cards' labels are distinct: 23456
        if len(uniqe_cards) == 5:
            return CARD_TYPES[0]

        # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        return CARD_TYPES[1]
        
    # to handle jokers,       
        


def part1(input_list):
    # parse input into tuples of strings and ints
    card_bid_tuples = [(card_str, int(num_str)) for card_str, num_str in [item.split(' ') for item in input_list]]

    # print(Hand(('T55J5', 5)).type,'|', Hand(('32T3K', 5)).type)
    # print(CARD_TYPES.index(Hand(('T55J5', 5)).type),'|', CARD_TYPES.index(Hand(('32T3K', 5)).type))
    # print(Hand(('T55J5', 5)) < Hand(('32T3K', 5)))
    
    h1 = Hand(('KQQQQ', 5))
    h2 = Hand(('KK9KK', 5))
    print(h1.card_type,'|', h2.card_type)
    print(CARD_TYPES.index(h1.card_type),'|', CARD_TYPES.index(h2.card_type))
    for self_card, other_card in zip(h1.card_str, h2.card_str):
        print(self_card, other_card)
        print(CARD_ORDERING.index(self_card), CARD_ORDERING.index(other_card))
        print(CARD_ORDERING.index(self_card) < CARD_ORDERING.index(other_card))
    print(h1 < h2)
    print()
    print(CARD_TYPES.index(h1.card_type),'|', CARD_TYPES.index(h2.card_type))
    
    game = Game(card_bid_tuples)
    print(game)
    # print(game.total_winnings())

    return game.total_winnings()


def part2(input_list):
    # Possibilities:
    # - Make all hand combinations basically nested loops for each joker
    #   saving the highest hand.
    # - There are probably fixed options. Like if it is all jokers, there's 
    #   only 1 best option. If there are 4 jokers, it's  the same, the best
    #   option is to copy the 1 non joker for 5 of a kind. Let's run with that!
    pass


def p07():
    test_filename1 = "inputs/07-test1.txt"
    test_filename2 = "inputs/07-test2.txt"
    filename = "inputs/07.txt"

    input_list_test1 = get_line_input_as_list(test_filename1, "string")
    input_list_test2 = get_line_input_as_list(test_filename2, "string")
    input_list = get_line_input_as_list(filename, "string")

    test_output1 = part1(input_list_test1)
    # test_output2 = part2(input_list_test2)

    output1 = part1(input_list)
    # 254013427 is too low
    # output2 = part2(input_list)

    return output1, None
    return test_output1, None
    return test_output1, test_output2
    return output1, output2
