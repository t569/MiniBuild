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
json_filename = config['JsonFileName']
log_file = config['LogDataBase']

c_files = [f for f in os.listdir(source_dir) if f.endswith('.c')]
cpp_files = [f for f in os.listdir(source_dir) if (f.endswith('.cpp') or f.endswith('.cxx'))]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # readfiles.compile_link_and_dump_dir(c_command, 'c', json_filename, source_dir + '\\Ctest\\', output_dir,ExecName='ctest', executeFlag=True)
    my_first_machine = compile.CompileMachine(cpp_command, json_filename, log_file,  source_dir, output_dir, 'c++')
    readfiles.change_attribute(my_first_machine, 'lazy_load', True)
    my_first_machine.compile_and_dump_each()
    my_first_machine.compile_and_dump_each()
    my_first_machine.compile_and_dump_each()
    my_first_machine.compile_and_dump_each()
    my_first_machine.compile_and_dump_each()
    my_first_machine.compile_and_dump_each()
    my_first_machine.compile_and_dump_each()









# TODO: handle the copying of output to test buffer
# TODO: implement testing
# TODO: multithreading
# TODO: make it all an easy to use class or something
