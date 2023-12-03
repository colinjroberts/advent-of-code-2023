from tools import (get_csv_line_input_as_list, get_line_input_as_list) 


def part1(input_list):
    
    thresholds = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    
    # Let's try to just brute force this one.
    result = 0
    for item in input_list:
        
        # Split out the first part of the string with the game number
        # and a list of all of the rounds
        split_input = item.split(':')
        game_number = int(split_input[0][5:])
        rounds = split_input[1].strip().split('; ')
        
        # Iterate over the rounds and make a note of
        # whether or not this game should be counted.
        # A game should be counted if the counts of all
        # colors are below the thresholds set above.
        count = True
        for round in rounds:
            values = round.split(', ')
            for value in values:
                n, color = value.split(' ')
                if thresholds[color] < int(n):
                    count = False
    
        # From the problem statement, we want to sum all 
        # games whose counts are within the thresholds
        if count:
            result += game_number
    return result

# More splitting and brute forcing!
def part2(input_list):
    result = 0
    for item in input_list:
        # Again, get the rounds. We don't care about game
        # number this time
        split_input = item.split(':')
        rounds = split_input[1].strip().split('; ')
        
        # 0 initialize dict of colors
        min_cubes = {
        'red': 0,
        'green': 0,
        'blue': 0,
        }
        
        # iterate over the rounds tracking the max
        # counts of each color
        for round in rounds:
            values = round.split(', ')
            for value in values:
                n, color = value.split(' ')
                if int(n) > min_cubes[color]:
                    min_cubes[color] = int(n)
        
        # This time, the problem wants the sum of the power
        # of each game, where power is the product of min
        # number of cubes in each game
        power = 1
        for color, count in min_cubes.items():
           power *= count
        result += power
    return result


def p02():
    test_filename1 = "inputs/02-test1.txt"
    test_filename2 = "inputs/02-test2.txt"
    filename = "inputs/02.txt"

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


