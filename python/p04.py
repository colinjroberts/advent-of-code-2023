from tools import (get_csv_line_input_as_list, get_line_input_as_list) 


def part1(input_list):
    total_score = 0
    for row in input_list:
        card_number, data = list(map(lambda s: s.strip(), row.split(':')))
        winning_numbers_s, found_numbers_s = list(map(lambda s: s.strip(), data.split('|')))
        winning_numbers = intify(winning_numbers_s.split(' '))
        found_numbers = intify(found_numbers_s.split(' '))

        row_score = 0
        for num in found_numbers:
            if num in winning_numbers:
                if row_score == 0:
                    row_score = 1
                else:
                    row_score *= 2
        total_score += row_score
    return total_score

def intify(list_of_num_strings):
    mostly_numstrs = [num_str.strip() for num_str in list_of_num_strings if num_str.isdigit()]
    numbers = [int(num_str.strip()) for num_str in mostly_numstrs]
    return numbers


def part2(input_list):
    # Scan the list once and build a dict of scores
    # Another dict keeps track of quantities of each card, all starting at 1
    
    pass


def p04():
    test_filename1 = "inputs/04-test1.txt"
    test_filename2 = "inputs/04-test2.txt"
    filename = "inputs/04.txt"

    input_list_test1 = get_line_input_as_list(test_filename1, "string")
    input_list_test2 = get_line_input_as_list(test_filename2, "string")
    input_list = get_line_input_as_list(filename, "string")

    test_output1 = part1(input_list_test1)
    # test_output2 = part2(input_list_test2)

    output1 = part1(input_list)
    # output2 = part2(input_list)

    return output1, None
    return test_output1, None
    return test_output1, test_output2
    return output1, output2
