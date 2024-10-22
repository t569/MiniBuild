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
    '~init_link_box': init_link_box_rule,
    '~link_to_dir_link_box': link_to_dir_link_box_rule,
    '~init_project': init_project_rule,
    '~compile_project': compile_project_to_object_files,
    '~link_project': link_project_to_dir_rule,
}

macro_file_name = "rufai.txt"
target_file_dir = '.\\rufai_files\\'
target_file_executables_dir = '\\executables\\'


# defined a helper function for skipping tabs and spaces
def skip_leading_tabs_and_spaces(line):
    count = 0
    for char in line:
        if char == ' ' or char == '\t':
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
    beginning_of_macro = skip_leading_tabs_and_spaces(macro[0])
    count = 0

    for char in macro[0][beginning_of_macro:]:
        if char == '~' and count == 0:
            continue

        elif char == '~' and count != 0:
            raise Exception(f"Invalid macro: Error at line : {macro[1]}")

        count += 1


def split_macros(macro_instance):
    # added leading space matching
    pattern = r'^[ \t]*(?P<command_name>~?\w+)\((?P<args_and_flags>[^)]*)\)'

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


def count_indent(target_macro):
    return skip_leading_tabs_and_spaces(target_macro[0])


def clean_macros(target_macros_to_expand):
    clean_macros_list = []
    for macro in target_macros_to_expand:
        # first handle the errors
        handle_macros_errors(macro)

        command = split_macros(macro[0])  # macro[1] is the line number
        clean_macro_to_append = [call_command_rule(command[0], commands_to_parse, command[1]), macro[1]]

        clean_macro_to_append[0].insert(0, count_indent(macro) * ' ')
        clean_macros_list.append(clean_macro_to_append)

    return clean_macros_list


# open the file and read it
with open(target_file_dir + macro_file_name, 'r') as macro_file:
    output = macro_file.read()

# expand the macros
lines = output.split('\n')

# collect the macros to expand
macros_to_expand = collect_macros(output)
# print(macros_to_expand)

# clean up the file
clean_macros_list = clean_macros(macros_to_expand)

# finally, write these lines back to the txt
# open the file and read it
with open(target_file_dir + macro_file_name, 'r') as macro_file:
    lines_read = macro_file.readlines()
# print(lines_read)

for items in clean_macros_list:
    # modify the lines in lines_read
    lines_read[items[1] - 1] = ''.join(str(item) for item in items[0])
    lines_read[items[1] - 1] += '\n'

# all that is left is to dump all this rubbish into a python file
with open(target_file_dir + target_file_executables_dir + macro_file_name.split('.')[0] + '.py', 'w') as python_file:
    python_file.writelines(lines_read)
