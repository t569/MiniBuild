import os

from dotenv import dotenv_values

import compile
from utils import readfiles

config = dotenv_values('./.env')

c_command = config['C_COMMAND']
cpp_command = config['CPP_COMMAND']
cc_command = config['CC_COMMAND']
output_dir = config['OUTPUT_DIR']
source_dir = config['SOURCE_DIR']
json_filename = config['ResultJsonFile']
log_file = config['LogDataBase']

# c_files = [f for f in os.listdir(source_dir) if f.endswith('.c')]
# cpp_files = [f for f in os.listdir(source_dir) if (f.endswith('.cpp') or f.endswith('.cxx'))]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    my_first_machine = compile.CompileMachine(cpp_command, json_filename,
                                              log_file,  source_dir,
                                              output_dir, file_type='c++')
    readfiles.change_attribute(my_first_machine, 'source_dir', source_dir + '\\Ctest\\')
    readfiles.change_attribute(my_first_machine, 'file_type', 'c')
    my_first_machine.compile_and_dump_exec(compile_dir_to_executable='ctest', executeFlag=True)

    my_second_machine = compile.CompileMachine.use_config('buildconfig.json')
    my_second_machine.compile_and_dump_exec()

# TODO: implement testing
# TODO: multithreading

