import os

import executefiles
import readfiles
from dotenv import dotenv_values

config = dotenv_values('./.env')

c_command = config['C_COMMAND']
cpp_command = config['CPP_COMMAND']
cc_command = config['CC_COMMAND']
output_dir = config['OUTPUT_DIR']
source_dir = config['SOURCE_DIR']
json_filename = config['JsonFileName']

c_files = [f for f in os.listdir(source_dir) if f.endswith('.c')]
cpp_files = [f for f in os.listdir(source_dir) if (f.endswith('.cpp') or f.endswith('.cxx'))]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #executefiles.execute_and_dump(json_filename, output_dir)
    # readfiles.compile_link_and_dump_dir(c_command, 'c', json_filename, source_dir + '\\Ctest\\', output_dir,ExecName='ctest', executeFlag=True)
    my_first_machine = readfiles.CompileMachine(cpp_command, json_filename, source_dir, output_dir, 'c++')
    my_first_machine.compile_and_dump()
    my_first_machine.compile_and_dump()
    readfiles.change_attribute(my_first_machine, 'lazy_load', True)
    my_first_machine.compile_and_dump()
    my_first_machine.compile_and_dump()
# DONE: implement a lazy load
# TODO: handle the copying of output to test buffer
# TODO: implement testing
# TODO: multithreading
# TODO: make it all an easy to use class or something
