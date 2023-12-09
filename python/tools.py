import string
import os
import re

def get_line_input_as_list(input_filename, type):
    """Used for parsing newline delimited input into a list"""
    output = []
    with open(input_filename) as f:
        output.extend(list(f))

    if type == "raw":
        return [x for x in output]
    elif type == "string":
        return [x.strip() for x in output]
    elif type == "int":
        int_output = []
        for item in output:
            while not item.isnumeric():
                item = item.strip(string.ascii_letters)
                item = item.strip()
            int_output.append(int(item.strip()))
        return int_output


def get_csv_line_input_as_list(input_filename, type):
    """Used for parsing comma delimited input into a list"""

    output = []
    with open(input_filename) as f:
        output.extend(list(f))

    if type == "raw":
        return [x for x in output[0].split(",")]
    elif type == "string":
        return [x.strip() for x in output[0].split(",")]
    elif type == "int":
        int_output = []
        for item in output[0].split(","):
            item = item.strip(string.ascii_letters)
            item = item.strip()
            int_output.append(int(item.strip()))
    return int_output

def build_day(day):
    """Builds a new day if there are no indicators that day already exists

    day: a day as an integer

    """
    def check_for_existing_day(day):
        if day == 0:
            return False

        # Check for that's day script
        try:
            with open(f"p{day:02d}.py") as f:
                return False
        except FileNotFoundError or FileExistsError:
            pass

        # Check for that day's input files
        try:
            with open(f"inputs/{day:02d}.txt") as f:
                return False
        except FileNotFoundError or FileExistsError:
            pass
        try:
            with open(f"inputs/{day:02d}-test.txt") as f:
                return False
        except FileNotFoundError or FileExistsError:
            pass

        # Check main for whether or not it shows up in import, dict, or message body
        try:
            with open("main.py") as f:
                for i, line in enumerate(f.readlines()):
                    line = line.strip()
                    if line == f"from p{day:02d} import p{day:02d}":
                        return False
                    elif line.endswith(f"{day}: p{day:02d}(),"):
                        return False
                    elif line.startswith("start, end =") and line.endswith(str(day)):
                        return False

        except FileNotFoundError or FileExistsError:
            return False

        return True

    def make_input_files(day):
        # Make empty input files
        with open(f"inputs/{day:02d}.txt", 'w') as f:
            f.write("")
        with open(f"inputs/{day:02d}-test1.txt", 'w') as f:
            f.write("")
        with open(f"inputs/{day:02d}-test2.txt", 'w') as f:
            f.write("")
        
    def make_script_file(day):
        script_template = f'from tools import (get_csv_line_input_as_list, get_line_input_as_list) \n\n\n\
def part1(input_list):\n\
    pass\n\n\n\
def part2(input_list):\n\
    pass\n\n\n\
def p{day:02d}():\n\
    test_filename1 = "inputs/{day:02d}-test1.txt"\n\
    test_filename2 = "inputs/{day:02d}-test2.txt"\n\
    filename = "inputs/{day:02d}.txt"\n\n\
    input_list_test1 = get_line_input_as_list(test_filename1, "string")\n\
    input_list_test2 = get_line_input_as_list(test_filename2, "string")\n\
    input_list = get_line_input_as_list(filename, "string")\n\n\
    test_output1 = part1(input_list_test1)\n\
    # test_output2 = part2(input_list_test2)\n\n\
    # output1 = part1(input_list)\n\
    # output2 = part2(input_list)\n\n\
    return test_output1, None\n\
    return output1, None\n\
    return test_output1, test_output2\n\
    return output1, output2\n'

        with open(f"p{day:02d}.py", 'w') as f:
            f.write(script_template)

    def make_new_main(day):
        new_main = []
        with open("main.py") as f:
            for line in f.readlines():
                import_match = re.match(rf".*(from p{day-1:02d} import p{day - 1:02d}).*", line)
                dict_match = re.match(rf".*({day-1}: p{day-1:02d}\(\)),.*", line)
                start_end_match = re.match(r'.*(start, end =).*', line)
                if import_match:
                    new_main.append(line)
                    new_main.append(f"from p{day:02d} import p{day:02d}\n")
                elif dict_match:
                    new_main.append(f"    # {day - 1}: p{day - 1:02d}(),\n")
                    new_main.append(f"    {day}: p{day:02d}(),\n")
                elif start_end_match:
                    new_main.append(f"    start, end = {day}, {day}\n")
                else:
                    new_main.append(line)

        # Write the new main file
        with open("main.py", "w") as f:
            f.write("".join(new_main))

    # by this point, we should know it is ok to start the process
    # of making new files and modifying main
    if not check_for_existing_day(day):
        return False
    make_script_file(day)
    make_input_files(day)
    make_new_main(day)

    return True

if __name__ == "__main__":
    build_day(7)
    pass
