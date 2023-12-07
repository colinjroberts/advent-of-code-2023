from tools import (get_csv_line_input_as_list, get_line_input_as_list) 
import math

# use the quadratic eq to figure out where the threshold for faster
# times are, then figure out how many times fall into that category
def fast_press_time_count(time, distance):
    plus_quad = abs((-time + math.sqrt(time**2 - 4*distance)) / 2)
    minus_quad = abs((-time - math.sqrt(time**2 - 4*distance)) / 2)
    return time - 1 - 2*int(plus_quad)

# use the quadratic eq to figure out where the threshold for faster
# times are, then figure out how many times fall into that category
def list_of_times(time, distance, fast = False):
    plus_quad = abs((-time + math.sqrt(time**2 - 4*distance)) / 2)
    return [ i for i in range(time) if 0 + plus_quad < i < time - plus_quad] 


def part1(input_list):
    # parse inputs
    times = [ int(n) for n in input_list[0].split(" ") if n not in ['Time:', '']]
    distances = [ int(d) for d in input_list[1].split(" ") if d not in ['Distance:', '']]
    
    # calculate the product of the number of faster times by
    # iterating over each time/distance pair and getting the full list of
    # press times
    faster_time_product = 1
    for t,d in zip(times, distances):
        faster_times = list_of_times(t, d)
        faster_time_product *= len(faster_times)
        
    return faster_time_product

    # Could also do this using the faster time method I wrote for part 2
    faster_time_product = 1
    for time, distance in zip(times, distances):
        faster_time_product *= fast_press_time_count(time, distance)
        
    return faster_time_product


def part2(input_list):
    # parse inputs
    time = int(''.join([ n for n in input_list[0].split(" ") if n not in ['Time:', '']]))
    distance = int(''.join([ d for d in input_list[1].split(" ") if d not in ['Distance:', '']]))
    return fast_press_time_count(time, distance)



def p06():
    test_filename1 = "inputs/06-test1.txt"
    test_filename2 = "inputs/06-test2.txt"
    filename = "inputs/06.txt"

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
