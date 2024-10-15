import platform
import subprocess
import os
import json
import executefiles


# we need to define a class

# this will solve the problem of calling lazy_load on the first execution pipeline

# this function is used to change attributes of the class
def change_attribute(instance, attribute, new_value):
    if hasattr(instance, attribute):
        setattr(instance, attribute, new_value)
    else:
        raise ValueError(f'type: {type(instance)} has no attribute: {attribute}')
def changes_attributes(instance, attributes: dict):
    for old_attr,new_attr in attributes:
        setattr(instance, old_attr, new_attr)

class CompileMachine:
    def files_to_compile(self, filetype):
        if filetype == 'c':
            return [f for f in os.listdir(self.source_dir) if f.endswith('.c')]

        elif filetype == 'c++':
            return [f for f in os.listdir(self.source_dir) if (f.endswith('.cpp') or f.endswith('.cxx'))]

    def __init__(self, command, json_filename, source_dir, output_dir, file_type, lazy_load=False):
        self.files = None
        self.command = command
        self.json_filename = json_filename
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.file_type = file_type
        self._number_of_compiles = 0
        if lazy_load:
            self.lazy_load = True
        else:
            self.lazy_load = False

    def lazy_load_func(self, json_filename) -> list:
        json_file = os.path.join('./', json_filename)
        lazy_load_log = []
        with open(json_file, 'r') as jsonFile:  # read all things that have errors and put them in a list
            intermediate = json.load(jsonFile)

            for elem in intermediate:
                if elem['compile_status'] == 'failure':
                    lazy_load_log.append(elem['name'][0])
        return lazy_load_log

    def compile_and_dump(self, executeFlag=False):
        compilation_results = []
        extension = ''
        if platform.system() == "Windows":
            extension = '.exe'

        # check if lazy load is active
        if self.lazy_load and self._number_of_compiles > 0:
            self.files = self.lazy_load_func(self.json_filename)
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
                result = subprocess.run(runcommands, capture_output=True, text=True, check=True)
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

                result_of_compilation['output'] = {"stdout": e.stdout,
                                                   "stderr": e.stderr}  # capture the error message; Error message of death!!!

            compilation_results.append(result_of_compilation)

        json_file = os.path.join('./', self.json_filename)
        with open(json_file, 'w') as jsonFile:
            json.dump(compilation_results, jsonFile, indent=4)
        self._number_of_compiles += 1


