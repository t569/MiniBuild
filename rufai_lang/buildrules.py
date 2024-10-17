def call_command_rule(command_rule, command_dict, *args, **kwargs):
    if command_rule in command_dict:
        return command_dict[command_rule](*args, **kwargs)


def init_build_box_rule(dictionary_of_args):
    replace_list = [dictionary_of_args['name'], " = ", "compile.CompileMachine.use_config", '(',
                    f"'{dictionary_of_args['use_config']}'", ')']

    # TODO: resolve relative path of import later

    return replace_list


def compile_build_box_rule(dictionary_of_args):
    replace_list = []
    replace_list.append(dictionary_of_args['name'])
    replace_list.append(".")
    replace_list.append("compile_and_dump_exec")
    replace_list.append("(")
    replace_list.append("compile_dir_to_executable")
    replace_list.append(" = ")
    if not dictionary_of_args['dir_to_exec']:   # dir_to_exec is false
        replace_list.append(dictionary_of_args['dir_to_exec'])
    else:
        replace_list.append(f"'{dictionary_of_args['dir_to_exec']}'")
    replace_list.append(")")

    return replace_list
