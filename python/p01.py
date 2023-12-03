from tools import get_line_input_as_list

def part1(input_list):
    # scan each character in the string looking for digits 
    output = []
    for i in input_list:
        output.append(int(first_digit(i) + last_digit(i)))

    return sum(output)


def first_digit(text):
    # return on the first digit found
    for item in text:
        if item.isdigit():
            return item
    raise ValueError("No first digit found")


def last_digit(text):
    # finding the last digit is the same as
    # finding the first digit of the reversed string!
    return first_digit(text[::-1])


def part2(input_list):
    # - Find all numbers/words in the string and take earliest position
    # - Find the first digit number, then check all substrings before it
    # - Scan checking all substrings for matches as you go
    # - given that I have limited matches, scan for all matches then choose
    #   first and last
    
    # Is there a data structure I could make that would make this easy?
    output = []

    for line in input_list:
        # Makes a list of tuples (digit/word, location)
        all_numbers = all_matches(line)
        
        # converts any word numbers to digits
        converted_numbers = convert_to_digits(all_numbers)
        
        # sorts the list based on the location the number occurs
        sorted_all_numbers = sorted(converted_numbers, key=lambda p: p[1])
        
        # Get first and last numbers
        first_number = sorted_all_numbers[0][0]
        last_number = sorted_all_numbers.pop()[0]
        
        output.append(int(first_number + last_number))
    return sum(output)


def all_matches(text):
    # For the sake of completion, let's find all matches!
    # In the end, I want a list of tuples with the matched 
    # item and the location it occurs at.
    
    items_to_search_for = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'one', 'two', 'three', 'four', 'five', 'six', 
        'seven', 'eight', 'nine', 'zero'
    ]

    matches = []
    
    # Check every possible slice in the string for the 
    # size of the word/digit I'm looking for
    for item in items_to_search_for:
        start = 0
        end = len(item)
        while start <= len(text) - len(item):
            if text[start:end] == item:
                matches.append( (item, start) )
            start += 1
            end += 1
    return matches

def convert_to_digits(num_digit_tuples):
    word_digits = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    
    result = []
    for n, i in num_digit_tuples:
        if n in word_digits.keys():
            result.append((word_digits[n], i))
        else:
            result.append((n, i))
    
    return result


def p01():
    test_filename1 = "inputs/01-test.txt"
    test_filename2 = "inputs/01-test2.txt"
    filename1 = "inputs/01.txt"
    
    test_input_list1 = get_line_input_as_list(test_filename1, "string")
    test_input_list2 = get_line_input_as_list(test_filename2, "string")
    input_list1 = get_line_input_as_list(filename1, "string")

    test_output1 = part1(test_input_list1)
    test_output2 = part2(test_input_list2)

    output1 = part1(input_list1)
    output2 = part2(input_list1)

    return output1, output2
    return test_output1, test_output2
