from tools import (get_csv_line_input_as_list, get_line_input_as_list) 
import math

# Admittedly, this is not one of my better solutions. Bad variable names,
# bad approach, but it does work, so that's not so bad!

class Mapping:
    def __init__(self, from_type, to_type, list_of_mapping_values):
        self.from_type = from_type
        self.to_type = to_type
        self.mappings = list_of_mapping_values
    
    def __str__(self):
        output = [f"from_type: {self.from_type} to_type: {self.to_type}"]
        print(self.mappings)
        for m in self.mappings:
            output.append(f"{m}")
        return '\n'.join(output)
    
    def __repr__(self):
        return str(self)
            
            
class MappingCollection:
    def  __init__(self, input_list):
        self.mappings = []
        self.build_mappings(input_list)

    def build_mappings(self, input_list):
        line_index = 2
        while line_index < len(input_list):
            if "map" in input_list[line_index]:
                map_name = input_list[line_index][:-5]
                from_type, to_type = map_name.split('-to-')
                line_index += 1

                list_of_mapping_values = []
                while line_index < len(input_list) and input_list[line_index] != '':
                    values = input_list[line_index].strip().split(' ')
                    output_start = int(values[0])
                    input_start = int(values[1])
                    map_range = int(values[2])
                    
                    list_of_mapping_values.append((output_start, input_start, map_range))
                    line_index += 1

                self.mappings.append(Mapping(from_type, to_type, list_of_mapping_values))
            line_index += 1
            
    def __str__(self):
        return '\n'.join([str(m) for m in self.mappings])
            
    def __repr__(self):
        return str(self)
    
    def run_map(self, mapping, input_value):
        return_value = input_value
        for output_start, input_start, map_range in mapping.mappings:
                if input_start <= input_value < (input_start + map_range):
                    return_value = input_value - input_start + output_start
                    break

        return return_value, mapping.to_type
    
    def run_map_backwards(self, mapping, input_value):
        return_value = input_value
        for input_start, output_start, map_range in mapping.mappings:
                if input_start <= input_value < (input_start + map_range):
                    return_value = input_value - input_start + output_start
                    break

        return return_value, mapping.from_type   
    
    
    # Takes an input value and a map type, then runs the value through
    # that map and returns a value and next map input type
    def run_forward(self, map_input_type, output_type, input_value):
        value = input_value
        cur_type = map_input_type
        while cur_type != output_type:
            # find the right map
            value_map = [x for x in self.mappings if x.from_type == cur_type][0]
            # map the value
            value, cur_type = self.run_map(value_map, value)
        return value

    def run_backward(self, map_input_type, output_type, input_value):
        value = input_value
        cur_type = map_input_type
        # print(f'starting with {map_input_type} #{value} looking for {output_type}')

        while cur_type != output_type:
            # find the right map
            value_map = [x for x in self.mappings if x.to_type == cur_type][0]
            # map the value
            value, cur_type = self.run_map_backwards(value_map, value)
            # print(f'cur_type {cur_type} value {value}')

        return value
            

def part1(input_list):
    # Each map works the same way, so one transformer function should
    # work for each type. Could calculate it all at run time or 
    # pre-generate all of them in some giant object (but looking at
    # the actual input, the numbers seem sufficiently big to not want
    # to do that.
    
    # Each transformation needs to take the thing to look up and the map
    # match using the start item and the range. If the input is within 
    # range, then run the transformation with modified mapping using the 
    # same offset, otherwise the output is the same
    
    # first step is to process the input
    seed_values = (int(i) for i in input_list[0].lstrip('seeds: ').split(' '))
    maps = MappingCollection(input_list)    
    
    # Find outputs
    minimum_value = math.inf
    for sv in seed_values:
        minimum_value = min(minimum_value, maps.run_forward('seed', 'location', sv))
    
    return minimum_value

def is_number_in_ranges(number, ranges):
    ranges.sort(key=lambda x: x[0])
    for smallest, largest in ranges:
        if smallest <= number <= largest:
            return True
    return False

def part2(input_list):
    # for part 2, I think the only thing that changes is the number
    # of seeds we need to check. Can this be brute forced?
    # No, or at least it really shouldn't. 
    # I have the maps!
    
    # Sort the last map by lowest output number, 
    # then go through maps backwards to get the largest and smallest seed that are in that map range
    # look through the inputs to see if any seeds map that location
    
    # Welp, in the end I brute forced it by trying all options of end locations until one matched a 
    # starting number. I
    
    # Build seed ranges into min, max pairs
    seed_ranges = [int(s) for s in input_list[0].lstrip('seeds: ').split(' ')]

    # Build min and max ranges of inputs for answer checking, sort by mins
    seed_range_index = 0
    seed_min_maxes = []
    while seed_range_index < len(seed_ranges):
        seed_min_maxes.append((seed_ranges[seed_range_index], seed_ranges[seed_range_index] + seed_ranges[seed_range_index+1] - 1))
        seed_range_index += 2
    seed_min_maxes.sort(key=lambda x: x[0])         
   
    # Build the maps from input
    maps = MappingCollection(input_list)    
    
    # Get the starts and stops of all of the location transformers 
    value_map = [x for x in maps.mappings if x.to_type == 'location'][0]

    # start at some location and start going up until the max mapped
    # location. There's only 4 billion, how long could it take?
    # (a few mintues was the answer)
    print('smallest values')
    value_map.mappings.sort(key=lambda x: x[0], reverse=True)
    # Starting where I left off after the first try
    i = 1000000
    end = max(value_map.mappings[0])
    while i <= end:
        seed_value = maps.run_backward('location', 'seed', i)
        if i % 100000 == 0:
            print(i, seed_value, end)
        if is_number_in_ranges(seed_value, seed_min_maxes):
            return i
        i += 1

    return None


def p05():
    test_filename1 = "inputs/05-test1.txt"
    test_filename2 = "inputs/05-test2.txt"
    filename = "inputs/05.txt"

    input_list_test1 = get_line_input_as_list(test_filename1, "string")
    input_list_test2 = get_line_input_as_list(test_filename2, "string")
    input_list = get_line_input_as_list(filename, "string")

    test_output1 = part1(input_list_test1)
    test_output2 = part2(input_list_test2)

    output1 = part1(input_list)
    output2 = part2(input_list)

    # return test_output1, test_output2
    return output1, output2
    # return test_output1, None
    return output1, None
