from tools import (get_csv_line_input_as_list, get_line_input_as_list) 

# Given a list of integers, recursively calculate the difference
# between each of the integers until all of the differences are 0s
def differentiate_list(list_of_ints, list_builder=None):
    # Base case, return if the input is a list of all 0s
    if set(list_of_ints) == {0}:
        return list_builder
    
    # Just starting helper, if no list_builder, make one
    if list_builder == None:
        list_builder = [list_of_ints]
            
    # Make a new list with all the differences
    new_list = []
    for i, item in enumerate(list_of_ints):
        # skip the first item
        if i == 0:
            continue
        
        # Subtract current number from previous number in list
        new_list.append(item - list_of_ints[i-1])

    list_builder.append(new_list)
    return differentiate_list(new_list, list_builder)


# Use the list of differences that goes down  to all 0s to 
# figure out what the next item in the list should be. 
# This could definitely be better parameterized / deduplicated
def extend_differentiated_list(list_of_differences, reverse=False):
    
    # For part 2
    if reverse:
        # iterate over each level of differences backwards starting with 0s
        amount_to_add = 0
        for i, lod in enumerate(list_of_differences[::-1]):
            # Add a zero to the beginning of list of zeros to get things
            # started, then move to the next loop
            if i == 0:
                lod.insert(0,0)
                continue
            
            # For every other loop, take the first element from the
            # previous level and subtract it from the first item from this layer
            amount_to_add = list_of_differences[::-1][i-1][0]
            lod.insert(0, lod[0] - amount_to_add)

    # For part 1
    else:
        amount_to_add = 0
        # iterate over each level of differences backwards starting with 0s
        for i, lod in enumerate(list_of_differences[::-1]):
            # Add a zero to the end of list of zeros to get things
            # started, then move to the next loop
            if i == 0:
                lod.append(0)
                continue
            
            # For every other loop, take the last element from the
            # previous level and add it to the last item from this layer
            amount_to_add = list_of_differences[::-1][i-1][-1]
            lod.append(lod[-1] + amount_to_add)

    return list_of_differences


def part1(input_list):
    # Convert input into a list of lists of ints
    list_of_list_of_ints = [[int(x) for x in line.split(' ')] for line in input_list]
    
    amended_lists = []
    for row in list_of_list_of_ints:
        
        # for each row in the input, figure out all of the 
        # differences between each number over and over until
        # they are all 0s
        list_of_differences = differentiate_list(row)
        
        # Calculate the amended list just in case / for print debugging
        proof_of_calculation = extend_differentiated_list(list_of_differences)
        
        # But only keep the first list because that is the top level one
        amended_lists.append(proof_of_calculation[0])

    # Now that we've modified each list by adding an item to the end of each, 
    # Calculate the sum using the first number from the top level of 
    # each amended list
    sum = 0
    for al in amended_lists:
        sum += al[-1]
    
    return sum   
 
def part2(input_list):
    # Convert input into a list of lists of ints
    list_of_list_of_ints = [[int(x) for x in line.split(' ')] for line in input_list]
    
    amended_lists = []
    for row in list_of_list_of_ints:
        # for each row in the input, figure out all of the 
        # differences between each number over and over until
        # they are all 0s
        list_of_differences = differentiate_list(row)

        # Calculate the amended list just in case / for print debugging
        proof_of_calculation = extend_differentiated_list(list_of_differences, True)

        # But only keep the first list because that is the top level one
        amended_lists.append(proof_of_calculation[0])

    # Now that we've modified each list by adding an item to the beginning, 
    # Calculate the sum using the first number from the top level of 
    # each amended list
    sum = 0
    for al in amended_lists:
        sum += al[0]
    
    return sum


def p09():
    test_filename1 = "inputs/09-test1.txt"
    test_filename2 = "inputs/09-test2.txt"
    filename = "inputs/09.txt"

    input_list_test1 = get_line_input_as_list(test_filename1, "string")
    input_list_test2 = get_line_input_as_list(test_filename2, "string")
    input_list = get_line_input_as_list(filename, "string")

    test_output1 = part1(input_list_test1)
    test_output2 = part2(input_list_test2)

    output1 = part1(input_list)
    output2  = part2(input_list)

    return output1, output2
    return test_output1, test_output2
    return output1, None
    return test_output1, None
