from tools import (get_csv_line_input_as_list, get_line_input_as_list) 
from typing import List

# Have a 2D grid of numbers and symbols. Need to sum all numbers
# that have a symbol in one or more cells adjacent to the number 
# (including diagonally).
# Options:
# - Scan for symbols then look around for numbers
#   - This one is a little easier for the main scan as it only 
#     needs to check one character at a time, but might end up
#     needing to deduplicate numbers
# - Scan for numbers and look around for symbols
#   - This one requires figuring out a whole number and its boundary 
#     up front, but after that deciding whether or not it should be 
#     included should be straight forward.
 

class Grid:
    def __init__(self, list_of_strings: List[str]):
        self.grid = self.gridify(list_of_strings)
        self.max_rows = len(self.grid)
        self.max_cols = len(self.grid[0])
        self.max_loc = self.max_rows * self.max_cols - 1
        self.known_symbol_indices = set()

    # Take list of strings and return list of lists
    # for easier data accessing later
    def gridify(self, input_list: list) -> List[List[str]]:
        return [list(row) for row in input_list]

    def is_valid_row(self, row):
        return row >= 0 and row < self.max_rows
    
    def is_valid_col(self, col):
        return col >= 0 and col < self.max_cols

    # loc is a 0-index absolute location in the grid
    # 0,  1,  2,  3
    # 4,  5,  6,  7
    # 8,  9, 10, 11
    # such that r0, c0 = l0, r0, c3 = l3, and r2, c3 = 11
    def loc_to_rowcol(self, loc: int) -> (int, int):
        return (loc//self.max_rows, loc % self.max_cols)

    def rowcol_to_loc(self, row: int, col: int) -> int:
        return col + (row * self.max_cols)

    def character_at(self, loc:int) -> str:
        row, col = self.loc_to_rowcol(loc)
        return self.grid[row][col]
    
    # Given a loc with a digit, find the starting loc of that number
    # Assumes numbers don't span rows

    def identify_start_of_number(self, loc:int) -> int:
        while self.character_at(loc).isdigit() and (loc % self.max_cols) >= 0: 
            loc -= 1

        return loc + 1
    
    # Given that the value at this column location is a
    # number, figure out how long the number is and return 
    # the value as a string
    # Assumes numbers don't span rows
    def identify_number(self, loc: int) -> str:
        num_string_builder = []
        while self.character_at(loc).isdigit() and (loc % self.max_cols) < self.max_cols:
            num_string_builder.append(self.character_at(loc))
            loc += 1

        return ''.join(num_string_builder)
    
    # Given a starting loc index for a number and the number's
    # length, find all valid indices (including numbers)
    # 0,  1,  2,  3
    # 4,  5,  6,  7
    # 8,  9, 10, 11
    # e.g. loc 0 has perimeter indices 1, 4, and 5
    #      loc 5 has perimeter indices 0, 1, 2, 4, 6, 8, 9, and 10
    def perimeter_indices_for_number(self, loc: int, word_size: int) -> List[int]:
        indices = set()

        for l in range(loc, loc+word_size):
            row, col = self.loc_to_rowcol(l)
            rows_to_check = [row-1, row, row+1]
            cols_to_check = [col-1, col, col+1]
            
            # currently, this will add every valid neighbor AND the 
            # loc itself which gets removed after
            for r in rows_to_check:
                if self.is_valid_row(r):
                    for c in cols_to_check:
                        if self.is_valid_col(c):
                            indices.add(self.rowcol_to_loc(r,c))
                            
            indices.remove(l)
        
        return list(indices)
        
    def perimeter_has_symbols(self, indices_to_check: List[str]) -> bool:
        for i in indices_to_check:
            if i in self.known_symbol_indices:
                return True
            
            c = self.character_at(i)
            if not c.isdigit() and c != '.':
                self.known_symbol_indices.add(i)

                return True
        return False

    def numbers_around_loc(self, loc):
        numbers = set()
        perimeter_indices = self.perimeter_indices_for_number(loc, 1)
        for i in perimeter_indices:
            if self.character_at(i).isdigit():
                start_of_number = self.identify_start_of_number(i)
                number = self.identify_number(start_of_number)
                numbers.add((number, start_of_number))
        return list(numbers)

def part1(input_list: list) -> int:
    
    grid = Grid(input_list)
    max_loc = grid.max_loc
    
    # Scan the list: 
    #  - identify whole, multi place numbers
    #  - determine whether it should be included
    #    - if so, add to running total
    running_total = 0
    
    # loc is absolute location in the grid
    # 1-indexed to avoid divide by 0 errors
    # 1,  2,  3,  4
    # 5,  6,  7,  8
    # 9, 10, 11, 12
    # such that the value at row 2, col 2 has loc 6
    loc = 0
    
    while loc < max_loc:
        word_size = 1
        
        # Look for numbers
        char = grid.character_at(loc)
        if char.isdigit():

            # If current value is a number, figure out where the number ends
            # This assumes numbers don't span lines
            number_as_str = grid.identify_number(loc)
            word_size = len(number_as_str)

            # Get perimeter indices
            perimeter_indices = grid.perimeter_indices_for_number(loc, word_size)
            # Check perimeter for symbols
            if grid.perimeter_has_symbols(perimeter_indices):

                running_total += int(number_as_str)

        # Increment location by 1 unless a number was found in which case increase
        # by that many (word_size)
        for i in range(word_size):
            loc += 1
    
    return running_total



def part2(input_list):
    # Find all of the *s adjacent to two numbers
    grid = Grid(input_list)
    max_loc = grid.max_loc
    
    # Scan the list: 
    #  - identify whole, multi place numbers
    #  - determine whether it should be included
    #    - if so, add to running total
    running_total = 0
    
    # loc is absolute location in the grid
    # 1-indexed to avoid divide by 0 errors
    # 1,  2,  3,  4
    # 5,  6,  7,  8
    # 9, 10, 11, 12
    # such that the value at row 2, col 2 has loc 6
    loc = 0
    
    while loc < max_loc:
        if grid.character_at(loc) == '*':
            # look around for numbers
            # numbers is list of tuples (number, loc) 
            numbers = grid.numbers_around_loc(loc)

            if len(numbers) == 2:
                running_total += int(numbers[0][0]) * int(numbers[1][0])
        loc += 1
    return running_total



def p03():
    test_filename1 = "inputs/03-test1.txt"
    test_filename2 = "inputs/03-test2.txt"
    filename = "inputs/03.txt"

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
