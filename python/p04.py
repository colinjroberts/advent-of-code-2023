from tools import (get_csv_line_input_as_list, get_line_input_as_list) 

def intify(list_of_num_strings):
    mostly_numstrs = [num_str.strip() for num_str in list_of_num_strings if num_str.isdigit()]
    numbers = [int(num_str.strip()) for num_str in mostly_numstrs]
    return numbers

class Deck:
    def __init__(self, input_list):
        # Do the work of part 1 to identify the number of matching
        # numbers in each input row (aka each card in the deck)
        self.row_matches_dict = self.row_scores(input_list)
        
        # Build a dict with each card number as the key and initialize its count to 1
        self.card_count_dict = dict([(k,1) for k, v in self.row_matches_dict.items()])

    def row_scores(self, input_list):
        row_matches = {}
        for row in input_list:
            card_number_s, data = list(map(lambda s: s.strip(), row.split(':')))
            card_number = int(card_number_s[4:])
            winning_numbers_s, found_numbers_s = list(map(lambda s: s.strip(), data.split('|')))
            winning_numbers = intify(winning_numbers_s.split(' '))
            found_numbers = intify(found_numbers_s.split(' '))

            match_count = 0
            for num in found_numbers:
                if num in winning_numbers:
                    match_count += 1
            row_matches[card_number] = match_count
        return row_matches
    
    # Scoring for part 1 of the problem
    def score_cards(self):
        total_score = 0
        for _, count in self.row_matches_dict.items():
            card_count = 0
            for i in range(count):
                if card_count == 0:
                    card_count = 1
                else:
                    card_count *= 2
            total_score += card_count
        return total_score
    
    # Go through the dict in number order (which in this case should also 
    # be insertion order for the dict, so I don't need to sort it or anything)
    # and add counts to subsequent matching cards
    def expand_counts(self):
        for card, count in self.row_matches_dict.items():
            for i in range(1, count+1):
                self.card_count_dict[card + i] += self.card_count_dict[card]


def part1(input_list):
    # This was the original, but moved it up to the class while working
    # on part 2
    # total_score = 0
    # for row in input_list:
    #     card_number, data = list(map(lambda s: s.strip(), row.split(':')))
    #     winning_numbers_s, found_numbers_s = list(map(lambda s: s.strip(), data.split('|')))
    #     winning_numbers = intify(winning_numbers_s.split(' '))
    #     found_numbers = intify(found_numbers_s.split(' '))

    #     row_score = 0
    #     for num in found_numbers:
    #         if num in winning_numbers:
    #             if row_score == 0:
    #                 row_score = 1
    #             else:
    #                 row_score *= 2
    #     total_score += row_score
    # return total_score
    deck = Deck(input_list)
    return deck.score_cards()


def part2(input_list):
    # Scan the list once and build a dict of scores
    # Another dict keeps track of quantities of each card, all starting at 1
    # These are part of Deck's constructor
    deck = Deck(input_list)
    deck.expand_counts()
    return sum(deck.card_count_dict.values())


def p04():
    test_filename1 = "inputs/04-test1.txt"
    test_filename2 = "inputs/04-test2.txt"
    filename = "inputs/04.txt"

    input_list_test1 = get_line_input_as_list(test_filename1, "string")
    input_list_test2 = get_line_input_as_list(test_filename2, "string")
    input_list = get_line_input_as_list(filename, "string")

    test_output1 = part1(input_list_test1)
    test_output2 = part2(input_list_test2)

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1, output2
    return test_output1, test_output2
    return test_output1, None
    return output1, None
