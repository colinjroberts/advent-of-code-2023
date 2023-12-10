from tools import (get_csv_line_input_as_list, get_line_input_as_list) 


def part1(input_list):
    list_of_list_of_ints = [[int(x) for x in line.split(' ')] for line in input_list]
    
    amended_lists = []
    for row in list_of_list_of_ints:
        list_of_differences = differentiate_list(row)
        # print(list_of_differences)
        
        # Calculate the amended list just in case
        proof_of_calculation = extend_differentiated_list(list_of_differences)
        
        # But only keep the first list because that is the top level one
        amended_lists.append(proof_of_calculation[0])

    # Calculate the sum using the last number from the top level of 
    # each amended list
    sum = 0
    for al in amended_lists:
        sum += al[-1]
    
    return sum

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
        
        new_list.append(item - list_of_ints[i-1])

    list_builder.append(new_list)
    return differentiate_list(new_list, list_builder)
    
def extend_differentiated_list(list_of_differences):
    # Add a zero to the list of zeros
    amount_to_add = 0
    for i, lod in enumerate(list_of_differences[::-1]):
        if i == 0:
            lod.append(0)
            continue
        
        amount_to_add = list_of_differences[::-1][i-1][-1]
        lod.append(lod[-1] + amount_to_add)

    return list_of_differences
    # Then work backwards through the lists 
    # Take the last number from the last list and add
    
    
def part2(input_list):
    pass


def p09():
    test_filename1 = "inputs/09-test1.txt"
    test_filename2 = "inputs/09-test2.txt"
    filename = "inputs/09.txt"

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
