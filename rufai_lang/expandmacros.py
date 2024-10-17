# this is the first file in my mini macro system for python build system MiniBuild!!!!!!!
import os
import re
from buildrules import *

# the command and the rule

commands_to_parse = {
    '~init_build_box':  init_build_box_rule,
    '~compile_build_box':   compile_build_box_rule,
}

macro_file_name = "rufai.txt"
target_file_dir = '.\\rufai_files\\'
target_file_executables_dir = '\\executables\\'

# open the file and read it
with open(target_file_dir + macro_file_name, 'r') as macro_file:
    output = macro_file.read()

# expand the macros
lines = output.split('\n')


def collect_macros(file_txt):
    to_expand = []
    line_count = 0
    for line in lines:
        line_count += 1
        if line:
            if line[0] == '~':
                to_expand.append([line, line_count])

    return to_expand

def handle_macros_errors(macro):
    count = 0
    for char in macro[0]:
        if char == '~' and count == 0:
            continue
        elif char == '~' and count != 0:
            raise Exception(f"Invalid Macro: Error at line: {macro[1]}")

        count += 1


macros_to_expand = collect_macros(output)

# clean up the file
def split_macros(macro_instance):
    pattern = r'(?P<command_name>~?\w+)\((?P<args_and_flags>[^)]*)\)'

    match = re.match(pattern, macro_instance.strip())

    if match:
        command_name = match.group('command_name')
        args_and_flags = match.group('args_and_flags')

        args = {}

        if args_and_flags:
            for arg in args_and_flags.split(','):
                key_value = arg.split('=')
                if len(key_value) == 2:
                    key, value = key_value[0].strip(), key_value[1].strip()
                    args[key] = value

        return command_name, args
    else:
        return None, None  # nothing to match


def clean_macros(macros_to_expand):
    clean_macros_list = []
    for macro in macros_to_expand:

        # first handle the errors
        handle_macros_errors(macro)
        command = split_macros(macro[0])  # macro[1] is the line number
        clean_macros_list.append([call_command_rule(command[0], commands_to_parse, command[1]), macro[1]])

    return clean_macros_list
        # TODO: parse the clean_macro_list properly

clean_macros_list = clean_macros(macros_to_expand)


# finally, write these lines back to the txt
# open the file and read it
with open(target_file_dir + macro_file_name, 'r') as macro_file:
    lines_read = macro_file.readlines()


for items in clean_macros_list:
    # modify the lines in lines_read
    lines_read[items[1] - 1] = ''.join(items[0])


# all that is left is to dump all this rubbish into a python file
with open(target_file_dir + target_file_executables_dir + macro_file_name.split('.')[0] + '.py', 'w') as python_file:
    python_file.writelines(lines_read)


