from tools import (get_csv_line_input_as_list, get_line_input_as_list) 


def part1(input_list):
    
    thresholds = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    
    result = 0
    for item in input_list:
        split_input = item.split(':')
        game_number = int(split_input[0][5:])
        rounds = split_input[1].strip().split('; ')
        
        print(game_number)
        count = True
        for round in rounds:
            values = round.split(', ')
            for value in values:
                print(value)
                n, color = value.split(' ')
                if thresholds[color] < int(n):
                    count = False
        if count:
            result += game_number
    return result


def part2(input_list):
    result = 0
    for item in input_list:
        split_input = item.split(':')
        rounds = split_input[1].strip().split('; ')
        
        max_cubes = {
        'red': 0,
        'green': 0,
        'blue': 0,
        }
        
        count = True
        for round in rounds:
            values = round.split(', ')
            for value in values:
                n, color = value.split(' ')
                if int(n) > max_cubes[color]:
                    max_cubes[color] = int(n)
        
        power = 1
        for color, count in max_cubes.items():
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


