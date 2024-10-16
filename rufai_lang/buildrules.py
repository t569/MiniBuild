def call_command_rule(command_rule, command_dict, *args, **kwargs):
    if command_rule in command_dict:
        return command_dict[command_rule](*args, **kwargs)


def init_build_box_rule(dictionary_of_args):
    replace_list = [dictionary_of_args['name'], " = ", "compile.CompileMachine.use_config", '(',
                    f"'{dictionary_of_args['use_config']}'", ')']

    # TODO: resolve relative path of import later

    return replace_list
