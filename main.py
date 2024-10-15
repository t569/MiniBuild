import os

import executefiles
import readfiles
from dotenv import dotenv_values

config = dotenv_values('./.env')

c_command = config['C_COMMAND']
cpp_command = config['CPP_COMMAND']

output_dir = config['OUTPUT_DIR']
source_dir = config['SOURCE_DIR']
json_filename = config['JsonFileName']

c_files = [f for f in os.listdir(source_dir) if f.endswith('.c')]
cpp_files = [f for f in os.listdir(source_dir) if (f.endswith('.cpp') or f.endswith('.cxx')) ]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #readfiles.compile_and_dump(cpp_command, json_filename, source_dir, output_dir, cpp_files,)
    #executefiles.execute_and_dump(json_filename, output_dir)
    readfiles.compile_and_dump_dir('cc', 'c', json_filename, source_dir + '\\Ctest\\', output_dir,ExecName='ctest')
