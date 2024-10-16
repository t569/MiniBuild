import platform
import os
import json
import typing
from utils.readfiles import lazy_load_func
from utils.readfiles import compile
from utils.logging import log_to_file

# redundant lol
from main import cc_command


class CompileMachine:
    def lazy_load_check_and_handle(self):
        if self.lazy_load and self._number_of_compiles > 0:
            self.files = lazy_load_func(self.json_filename)
            print(f"Lazy load activated for compilation...")
        else:
            self.files = self.files_to_compile(self.file_type)

    def files_to_compile(self, filetype):
        if filetype == 'c':
            return [f for f in os.listdir(self.source_dir) if f.endswith('.c')]

        elif filetype == 'c++':
            return [f for f in os.listdir(self.source_dir) if (f.endswith('.cpp') or f.endswith('.cxx'))]

    def __init__(self, command, json_filename, log_file, source_dir, output_dir, file_type, lazy_load=False,
                 compile_dir_to_executable=False):
        self.files = None
        self.command = command
        self.multi_command = cc_command
        self.json_filename = json_filename
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.file_type = file_type
        self.log_file = log_file
        self._number_of_compiles = 0
        self.os_type = platform.system()
        if lazy_load:
            self.lazy_load = True
        else:
            self.lazy_load = False

        if compile_dir_to_executable:
            self.dir_to_executable = True
        else:
            self.dir_to_executable = False

    def compile_and_dump_exec_each(self, executeFlag=False):
        compilation_results = []
        extension = ''
        if self.os_type == "Windows":
            extension = '.exe'

        # check if lazy load is active
        self.lazy_load_check_and_handle()

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

            result_of_compilation = compile(runcommands=runcommands,
                                            execute=executeFlag,
                                            results=result_of_compilation,
                                            file_to_compile=file,
                                            output_bin=output_binary,
                                            os_type=self.os_type)

            compilation_results.append(result_of_compilation)

        json_file = os.path.join('./', self.json_filename)
        with open(json_file, 'w') as jsonFile:
            json.dump(compilation_results, jsonFile, indent=4)
        self._number_of_compiles += 1

        # logging logic
        log_to_file(json_file, self.log_file, self.lazy_load)

    def compile_and_dump_exec_dir(self, executeFlag=False, ExecName='a'):
        compilation_results = []
        extension = ''
        if self.os_type != "Windows":
            if ExecName == 'a':
                extension = '.out'

        extension = '.exe'  # will evaluate if we are on windows

        # lang_type is list
        files_to_compile = self.files_to_compile(filetype=self.file_type)
        runcommands = [self.multi_command]
        for file in files_to_compile:
            runcommands.append(os.path.join(self.source_dir, file))

        runcommands.append('-o')
        output_binary = os.path.join(self.output_dir, ExecName)
        runcommands.append(output_binary)

        result_of_compilation = {
            'dir': [self.source_dir, ExecName + extension],
            'compile_link_status': '',
            'output': '',
        }
        # check if lazy load is active
        self.lazy_load_check_and_handle()

        # compilation process
        result_of_compilation = compile(runcommands=runcommands,
                                        execute=executeFlag,
                                        file_to_compile=self.source_dir,
                                        os_type=self.os_type,
                                        results=result_of_compilation,
                                        output_bin=output_binary)

        compilation_results.append(result_of_compilation)

        json_file = os.path.join('./', self.json_filename)
        with open(json_file, 'w') as jsonFile:
            json.dump(compilation_results, jsonFile, indent=4)

        self._number_of_compiles += 1

        # logging logic
        log_to_file(json_file, self.log_file, self.lazy_load)

    def compile_and_dump_exec(self, compile_dir_to_executable: typing.Union[str, bool] = False, executeFlag=False):

        if compile_dir_to_executable:
            self.compile_and_dump_exec_dir(executeFlag=executeFlag, ExecName=compile_dir_to_executable)

        else:
            self.compile_and_dump_exec_each(executeFlag=executeFlag)

