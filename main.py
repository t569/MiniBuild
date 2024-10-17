import os

from dotenv import dotenv_values

import build
import utils.executefiles
from utils import readfiles

config = dotenv_values('./.env')

c_command = config['C_COMMAND']
cpp_command = config['CPP_COMMAND']
cc_command = config['CC_COMMAND']
output_dir = config['OUTPUT_DIR']
output_dir_executables = config['OUTPUT_DIR'] + config['EXECUTABLES_DIR']
output_dir_object_files = config['OUTPUT_DIR'] + config['OBJECTFILES_DIR']
source_dir = config['SOURCE_DIR']
json_filename = config['RESULT_JSON_FILE']
log_file = config['LOG_DATABASE']

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
    my_first_machine = build.CompileMachine(cpp_command, json_filename,
                                            log_file, source_dir,
                                            output_dir, file_type='c++', lazy_load=True)
    readfiles.change_attribute(my_first_machine, 'source_dir', source_dir + '\\Ctest\\')
    readfiles.change_attribute(my_first_machine, 'file_type', 'c')
    my_first_machine.compile_and_dump_exec(compile_dir_to_executable='ctest', executeFlag=True)

    my_second_machine = build.CompileMachine.use_config('buildconfig.json')
    my_second_machine.compile_and_dump_exec(executeFlag=True)

    print(my_second_machine.lazy_load)
    print(my_first_machine.lazy_load)

    # compile_dir_to_executable not logging properly
     my_third_machine = build.CompileMachine.use_config('buildconfig.json')
    """

    my_fourth_machine = build.CompileMachine(c_command, json_filename, log_file, source_dir, output_dir, file_type='c',recursive_compile_dir=True)
    readfiles.change_attribute(my_fourth_machine, 'output_dir', output_dir_object_files)
    my_fourth_machine.compile_to_obj_and_dump()


# TODO: search through a dir and recursively add all the files to be compiled
# TODO: implement logic for non-lazy loading
# TODO: resolve the import/copying of the rufai lang file content (stall this)
# TODO: implement testing
# TODO: multithreading
