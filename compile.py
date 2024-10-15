import platform
import subprocess
import os
import json
from utils import executefiles
from utils.readfiles import lazy_load_func
from utils.logging import log_to_file

class CompileMachine:
    def files_to_compile(self, filetype):
        if filetype == 'c':
            return [f for f in os.listdir(self.source_dir) if f.endswith('.c')]

        elif filetype == 'c++':
            return [f for f in os.listdir(self.source_dir) if (f.endswith('.cpp') or f.endswith('.cxx'))]


    def __init__(self, command, json_filename, log_file, source_dir, output_dir, file_type, lazy_load=False, compile_dir_to_executable=False):
        self.files = None
        self.command = command
        self.json_filename = json_filename
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.file_type = file_type
        self.log_file =log_file
        self._number_of_compiles = 0
        if lazy_load:
            self.lazy_load = True
        else:
            self.lazy_load = False

        if compile_dir_to_executable:
            self.dir_to_executable = True
        else:
            self.dir_to_executable = False

    def compile_and_dump_each(self, executeFlag=False):
        compilation_results = []
        extension = ''
        if platform.system() == "Windows":
            extension = '.exe'

        # check if lazy load is active
        if self.lazy_load and self._number_of_compiles > 0:
            self.files = lazy_load_func(self.json_filename)
            print(f"Lazy load activated for compilation...")
        else:
            self.files = self.files_to_compile(self.file_type)

        # compilation process
        for file in self.files:
            source_file = os.path.join(self.source_dir, file)
            output_binary = os.path.join(self.output_dir, file.split('.')[0])

            runcommands = [self.command, source_file, '-o', output_binary]

            result_of_compilation = {
                'name': [file, file.split('.')[0] + extension],
                'compile_status': '',
                'output': '',
            }
            try:
                subprocess.run(runcommands, capture_output=True, text=True, check=True)
                print(f"Compilation of {file} successful")
                result_of_compilation['compile_status'] = 'success'

                if executeFlag:
                    print(f"Executing {output_binary}...")
                    stdout, stderr = executefiles.execute(platform.system(), output_binary)
                    result_of_compilation['output'] = {"stdout": stdout, "stderr": stderr}

                else:
                    result_of_compilation['output'] = ''

            except subprocess.CalledProcessError as e:
                print(f"Error during compilation of {file}")
                result_of_compilation['compile_status'] = 'failure'

                # capture the error message; Error message of death!!!
                result_of_compilation['output'] = {"stdout": e.stdout,
                                                   "stderr": e.stderr}
            compilation_results.append(result_of_compilation)

        json_file = os.path.join('./', self.json_filename)
        with open(json_file, 'w') as jsonFile:
            json.dump(compilation_results, jsonFile, indent=4)
        self._number_of_compiles += 1

        # logging logic
        log_to_file(json_file, self.log_file, self.lazy_load)


    # TODO: CONFIGURE THIS FUNCTION

    def compile_and_dump_dir(self, executeFlag=False, ExecName='a'):
        compilation_results = []
        extension = ''
        if platform.system() != "Windows":
            if ExecName == 'a':
                extension = '.out'

        extension = '.exe'  # will evaluate if we are on windows

        # lang_type is list
        files_to_compile = self.files_to_compile(filetype=self.file_type)
        runcommands = [self.command]
        for file in files_to_compile:
            runcommands.append(os.path.join(self.source_dir, file))

        runcommands.append('-o')
        output_binary = os.path.join(self.output_dir, ExecName)
        runcommands.append(output_binary)

        result_of_compilation = {
            'dir': [self.command, ExecName + extension],
            'compile_link_status': '',
            'output': '',
        }

        try:
            subprocess.run(runcommands, capture_output=True, text=True, check=True)
            print(f"Compilation of {self.source_dir} successful")
            result_of_compilation['compile_link_status'] = 'success'

            if executeFlag:
                print(f"Executing {output_binary}...")
                stdout, stderr = executefiles.execute(platform.system(), output_binary)
                result_of_compilation['output'] = {"stdout": stdout, "stderr": stderr}

            else:
                result_of_compilation['output'] = ''

        except subprocess.CalledProcessError as e:
            print(f"Error during compilation of {self.source_dir}")
            result_of_compilation['compile_link_status'] = 'failure'

            result_of_compilation['output'] = {"stdout": e.stdout,
                                               "stderr": e.stderr}  # capture the error message; Error message of death!!!

        compilation_results.append(result_of_compilation)

        json_file = os.path.join('./', self.json_filename)
        with open(json_file, 'w') as jsonFile:
            json.dump(compilation_results, jsonFile, indent=4)
