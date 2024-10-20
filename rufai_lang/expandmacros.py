# this is the first file in my mini macro system for python build system MiniBuild!!!!!!!
import os
import re
import ast
from buildrules import *

# the command and the rule

commands_to_parse = {
    '~init_build_box': init_build_box_rule,
    '~compile_build_box': compile_build_box_rule,
    '~execute_build_box': execute_build_box_rule,
}

macro_file_name = "rufai.txt"
target_file_dir = '.\\rufai_files\\'
target_file_executables_dir = '\\executables\\'


def skip_leading_tabs_and_spaces(line):
    count = 0
    for char in line:
        if char == ' ':
            count += 1
        else:
            break
    return count


def collect_macros(file_txt):
    to_expand = []
    line_count = 0
    for line in lines:
        line_count += 1
        if line:
            # remove all the leading spaces
            if line[skip_leading_tabs_and_spaces(line)] == '~':
                to_expand.append([line, line_count])

    return to_expand


def handle_macros_errors(macro):
    begining_of_macro = skip_leading_tabs_and_spaces(macro[0])
    count = 0

    for char in macro[0][begining_of_macro:]:
        if char == '~' and count == 0:
            continue

        elif char == '~' and count != 0:
            raise Exception(f"Invalid macro: Error at line : {macro[1]}")

        count += 1


# TODO: check usage (1 usage) for the TODOs
def split_macros(macro_instance):
    pattern = r'(?P<command_name>~?\w+)\((?P<args_and_flags>[^)]*)\)'

    match = re.match(pattern, macro_instance.strip())

    if match:
        command_name = match.group('command_name')
        args_and_flags = match.group('args_and_flags')

        args = {}

        if args_and_flags:

            # match key value pairs also allows nested structures
            key_value_pattern = r'(?P<key>\w+)\s*=\s*(?P<value>.+?)(?=,\s*\w+=|$)'
            for kv_match in re.finditer(key_value_pattern, args_and_flags):
                key_value = kv_match.group('key').strip()
                value = kv_match.group('value').strip()

                # evaluate all the python literals with ast
                try:
                    value = ast.literal_eval(value)

                except (ValueError, SyntaxError):
                    # if we can't evaluate value keep it as string
                    pass
                args[key_value] = value

        return command_name, args
    else:
        return None, None  # nothing to match


def clean_macros(target_macros_to_expand):
    clean_macros_list = []
    for macro in target_macros_to_expand:
        # first handle the errors
        handle_macros_errors(macro)
        # TODO: modify the split_macros function to recognise leading tabs and spaces
        command = split_macros(macro[0])  # macro[1] is the line number
        print(command)
        print("00000000000000000000")
        clean_macros_list.append([call_command_rule(command[0], commands_to_parse, command[1]), macro[1]])

    return clean_macros_list


# open the file and read it
with open(target_file_dir + macro_file_name, 'r') as macro_file:
    output = macro_file.read()

# expand the macros
lines = output.split('\n')

# defined a helper function for skipping tabs and spaces



# collect the macros to expand
macros_to_expand = collect_macros(output)

# clean up the file

# TODO: make the macros include leading spaces: check clean_macros function
clean_macros_list = clean_macros(macros_to_expand)
print(clean_macros_list)

# finally, write these lines back to the txt
# open the file and read it
with open(target_file_dir + macro_file_name, 'r') as macro_file:
    lines_read = macro_file.readlines()

for items in clean_macros_list:
    # modify the lines in lines_read
    lines_read[items[1] - 1] = ''.join(str(item) for item in items[0])

# all that is left is to dump all this rubbish into a python file
with open(target_file_dir + target_file_executables_dir + macro_file_name.split('.')[0] + '.py', 'w') as python_file:
    python_file.writelines(lines_read)
