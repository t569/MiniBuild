# this is to keep record of all the build boxes active
# TODO: FIND A WAY TO INTEGRATE THIS INTO THE MAIN FILE PIPELINE
meta_data = {'build_box': {}}


def call_command_rule(command_rule, command_dict, *args, **kwargs):
    if command_rule in command_dict:
        return command_dict[command_rule](*args, **kwargs)


def init_build_box_rule(dictionary_of_args):
    replace_list = [dictionary_of_args['name'], " = ", "build.BuildMachine.use_config", '(',
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
        replace_list.append(",")
    else:
        # dump as a string
        replace_list.append(f"'{dictionary_of_args['dir_to_exec']}'")

        # now add to meta_data: will need it later
        meta_data['build_box'][f"{dictionary_of_args['name']}"] = dictionary_of_args['dir_to_exec']
        print(meta_data)
        replace_list.append(",")

    if 'execute' in dictionary_of_args:
        replace_list.append("executeFlag")
        replace_list.append("=")
        replace_list.append(dictionary_of_args['execute'])
        replace_list.append(",")

    if 'include_obj_files' in dictionary_of_args:
        replace_list.append("include_obj_files")
        replace_list.append("=")
        replace_list.append(dictionary_of_args['include_obj_files'])
        replace_list.append(",")

    replace_list.append(")")
    return replace_list


# resolve all the imports dynamically
def resolve_all_imports():
    pass


def execute_build_box_rule(dictionary_of_args):
    replace_list: list = []
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
        replace_list.append(meta_data['build_box'][f"{dictionary_of_args['name']}"])
    except KeyError:
        raise KeyError(f"No build box system named: {dictionary_of_args['name']}")
    replace_list.append('"')
    replace_list.append(',')

    replace_list.append("extra_args")
    replace_list.append('=')
    replace_list.append(f"{dictionary_of_args['extra_args']}")
    # print(dictionary_of_args)

    replace_list.append(')')

    return replace_list


# LINKING PIPELINE
def init_link_box_rule(dictionary_of_args):
    replace_list = [dictionary_of_args['name'], " = ", "linker.LinkerMachine.use_config", '(',
                    f"'{dictionary_of_args['use_config']}'", ')']

    return replace_list


def link_to_dir_link_box_rule(dictionary_of_args):
    replace_list: list = []
    replace_list.append(dictionary_of_args['name'])
    replace_list.append('.')
    replace_list.append("link_dir_to_exec")
    replace_list.append('(')
    if 'project_name' in dictionary_of_args:
        replace_list.append("project_name")
        replace_list.append('=')
        replace_list.append(dictionary_of_args['project_name'])
        replace_list.append(',')

    if 'execute' in dictionary_of_args:
        if dictionary_of_args['execute']:
            replace_list.append("executeFlag")
            replace_list.append('=')
            replace_list.append(dictionary_of_args['execute'])
            replace_list.append(',')

    if 'extra_run_args' in dictionary_of_args:
        if dictionary_of_args['extra_run_args'] is not None and type(dictionary_of_args['extra_run_args']) is list:
            replace_list.append("extra_run_args")
            replace_list.append('=')
            replace_list.append(f"{dictionary_of_args['extra_run_args']}")
            replace_list.append(',')

    replace_list.append(')')

    return replace_list


# PROJECT PIPELINE
def init_project_rule(dictionary_of_args):
    replace_list: list = []
    replace_list = [dictionary_of_args['name'], " = ", "project.Project", '(',
                    'build_config', '=',
                    f"'{dictionary_of_args['build_config']}'",
                    ',',
                    'linker_config', '=',
                    f"'{dictionary_of_args['linker_config']}'", ')']
    return replace_list


def compile_project_to_object_files(dictionary_of_args):
    replace_list: list = []
    replace_list.append(dictionary_of_args['name'])
    replace_list.append('.')
    replace_list.append('compile_to_object_files')
    replace_list.append('(')
    replace_list.append(')')
    return replace_list


def link_project_to_dir_rule(dictionary_of_args):
    replace_list: list = []
    replace_list.append(dictionary_of_args['name'])
    replace_list.append('.')
    replace_list.append('link_to_executable')
    replace_list.append('(')
    replace_list.append(')')
    return replace_list
