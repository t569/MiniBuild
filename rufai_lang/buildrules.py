# this is to keep record of all the build boxes active
meta_data = {}

def call_command_rule(command_rule, command_dict, *args, **kwargs):
    if command_rule in command_dict:
        return command_dict[command_rule](*args, **kwargs)


def init_build_box_rule(dictionary_of_args):
    replace_list = [dictionary_of_args['name'], " = ", "build.CompileMachine.use_config", '(',
                    f"'{dictionary_of_args['use_config']}'", ')']

    # TODO: resolve relative path of import later

    return replace_list


def compile_build_box_rule(dictionary_of_args):
    replace_list: list = []
    replace_list.append(dictionary_of_args['name'])
    replace_list.append(".")
    replace_list.append("compile_and_dump_exec")
    replace_list.append("(")
    replace_list.append("compile_dir_to_executable")
    replace_list.append("=")
    if not dictionary_of_args['dir_to_exec']:  # dir_to_exec is false
        replace_list.append(dictionary_of_args['dir_to_exec'])
    else:
        # dump as a string
        replace_list.append(f"'{dictionary_of_args['dir_to_exec']}'")

        # now add to meta_data: will need it later
        meta_data[f"{dictionary_of_args['name']}"] = dictionary_of_args['dir_to_exec']

    replace_list.append(",")
    if dictionary_of_args['execute']:
        replace_list.append("executeFlag")
        replace_list.append("=")
        replace_list.append(dictionary_of_args['execute'])
    replace_list.append(")")

    return replace_list


# resolve all the imports dynamically
def resolve_all_imports():
    pass


def execute_build_box_rule(dictionary_of_args):
    replace_list:list = []
    # change alot of the boilerplate code
    replace_list.append("utils")
    replace_list.append('.')
    replace_list.append("executefiles")
    replace_list.append('.')
    replace_list.append("execute")
    replace_list.append('(')
    replace_list.append("os_type")
    replace_list.append('=')
    replace_list.append(f"{dictionary_of_args['name']}")
    replace_list.append('.')
    replace_list.append("os_type")
    replace_list.append(',')

    replace_list.append("executable_path")
    replace_list.append('=')
    # we need to get the output_dir + name of the file being compiled
    # output_dir + file
    replace_list.append(f"{dictionary_of_args['name']}")
    replace_list.append('.')
    replace_list.append("output_dir")
    replace_list.append('+')
    replace_list.append('"')
    try:
        replace_list.append(meta_data[f"{dictionary_of_args['name']}"])
    except KeyError:
        raise KeyError(f"No build box system named: {dictionary_of_args['name']}")
    replace_list.append('"')
    replace_list.append(',')

    replace_list.append("extra_args")
    replace_list.append('=')
    replace_list.append(f"{dictionary_of_args['extra_args']}")
    print(dictionary_of_args)

    replace_list.append(')')

    return replace_list
