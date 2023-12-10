from tools import (get_csv_line_input_as_list, get_line_input_as_list) 
from math import gcd

def part1(input_list):
    # Take first lin of input as the directions 
    directions = input_list[0]
    
    # Convert the L's to 0's and R's to 1's
    int_directions = [0 if d == 'L' else 1 for d in directions]
    
    # Use the remaining lines of the file to build a dict
    # with the nodes (AAA, BBB, ... ZZZ) as values 
    # and the tuple of options as the keys
    node_dict = {}
    for direction_tuple in input_list[2:]:
        label, nodes = direction_tuple.split(' = ')
        node_dict[label] = (nodes.strip('()').split(', '))

    # Start at the first node and go until ZZZ is found
    # At each step, choose the appropriate direction 
    # (step % # of directions) and use that direction
    # to update the current "location".
    cur = 'AAA'
    steps = 0
    while cur != 'ZZZ':
        # choose the right item from the list of directions
        # (that has been converted from L/Rs to 0/1s)
        # given how many steps we've taken (looping as needed)
        i = (steps) % len(int_directions)
        int_direction = int_directions[i]
        
        # Set the current node to be the "left" or "right"
        # node from the tuple value in node_dict at the key
        # corresponding to current index. 
        cur = node_dict[cur][int_direction]
        steps += 1
    
    return steps


def part2(input_list):
    # Take first lin of input as the directions 
    directions = input_list[0]
    
    # Convert the L's to 0's and R's to 1's
    int_directions = [0 if d == 'L' else 1 for d in directions]
    
    # Use the remaining lines of the file to build a dict
    # with the nodes (AAA, BBB, ... ZZZ) as values 
    # and the tuple of options as the keys
    node_dict = {}
    for direction_tuple in input_list[2:]:
        label, nodes = direction_tuple.split(' = ')
        node_dict[label] = (nodes.strip('()').split(', '))

    # Get all of the starting points, let's call these cursors
    cursors = [l for l in node_dict.keys() if l[2] == 'A' ]

    # Brute force it! Work until all of them end with Z.
    # At each step (i), 
    # i = 0
    # steps = 0
    # while not all_end_in_z(cursors):
    #     int_direction = int_directions[i]
    #     # print(f'{cursors}')

    #     for cur_i, cur in enumerate(cursors):
    #         cursors[cur_i] = node_dict[cur][int_direction]
    #     i = (i + 1) % len(int_directions)
    #     steps += 1
    # return steps
    
    # Ok, that doesn't seem like it's going to work. 
    # Second option: calculate the number of steps it takes for each
    # path to get to Z, then do some math.
    i = 0
    results = {}
    for cur_i, cur in enumerate(cursors):
        steps = 0

        while cur[2] != 'Z':
            # choose the right item from the list of directions
            # (that has been converted from L/Rs to 0/1s)
            # given how many steps we've taken (looping as needed)
            i = (steps) % len(int_directions)
            int_direction = int_directions[i]
            
            # Set the current node to be the "left" or "right"
            # node from the tuple value in node_dict at the key
            # corresponding to current index. 
            cur = node_dict[cur][int_direction]
            steps += 1
        results[cur] = steps

    print(f'{results}')

    # Now that we know how many steps it takes to get to ZZZ from each
    # starting path, find the least common multiple among them
    least_common_multiple = 1
    for _, step_count in results.items():
        least_common_multiple = least_common_multiple * step_count // gcd(least_common_multiple, step_count)

    return least_common_multiple

# This isn't used in the final answer, but was used for a hot second while
# trying to brute force it.
def all_end_in_z(list_of_nodes):
    return len(list_of_nodes) == len([n for n in list_of_nodes if n[2] == 'Z'])


def p08():
    test_filename1 = "inputs/08-test1.txt"
    test_filename2 = "inputs/08-test2.txt"
    filename = "inputs/08.txt"

    input_list_test1 = get_line_input_as_list(test_filename1, "string")
    input_list_test2 = get_line_input_as_list(test_filename2, "string")
    input_list = get_line_input_as_list(filename, "string")

    test_output1 = part1(input_list_test1)
    test_output2 = part2(input_list_test2)

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1, output2
    return test_output1, test_output2
    return output1, None
    return test_output1, None
