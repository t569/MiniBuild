import platform
import os
import json
import typing
from utils.readfiles import lazy_load_func
from utils.readfiles import compile
from utils.logging import log_to_file
# redundant lol
from main import cc_command


# please if you are reading this code to understand, start from here and the function compile_and_dump_exec
class CompileMachine:
    def lazy_load_check_and_handle(self):
        if self.lazy_load and self._number_of_compiles > 0:
            self.files = lazy_load_func(self.json_filename)
            print(f"Lazy load activated for compilation...")
        else:
            self.files = self.files_to_compile(self.file_type, recursive_compile_dir=self.recursive_compile_dir)

    def resolve_dir(self, directory_name: str, file_types: list) -> [str]:

        output_list: list = []
        # list all the files in a dir
        for i in os.listdir(directory_name):
            absolute_i_path = os.path.join(directory_name, i)
            if os.path.isfile(absolute_i_path):  # if it is a file and it matches the file type
                if self.is_filetype(file_types, absolute_i_path):
                    output_list.append(absolute_i_path)

            else:  # else it is a directory
                # ignore .folder folders
                if i[0] == '.':
                    continue
                output_list.extend(self.resolve_dir(absolute_i_path + "\\\\", file_types))
        return output_list

    def is_filetype(self, filetype: list[str], file: str):
        for extension in filetype:
            if file.endswith(extension):
                return True
        return False

    def files_to_compile(self, filetype, recursive_compile_dir):
        extensions = []

        if filetype == 'c':
            extensions = ['.c']
        elif filetype == 'c++':
            extensions = ['.cpp', '.cxx']

        if recursive_compile_dir:
            return self.resolve_dir(self.source_dir, extensions)

        else:
            return [f for f in os.listdir(self.source_dir) if self.is_filetype(extensions, f)]

    def __init__(self, command, json_filename, log_file, source_dir, output_dir, file_type, lazy_load=False,
                 compile_dir_to_executable=False, recursive_compile_dir=False, output_dir_executables=None, output_dir_objectfiles=None):
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

        # note this flag only works for compile_and_dump_exec_dir
        if recursive_compile_dir:
            self.recursive_compile_dir = True
        else:
            self.recursive_compile_dir = False

        if output_dir_executables is None:
            self.output_dir_executables = output_dir
        else:
            self.output_dir_executables = output_dir_executables
        if output_dir_objectfiles is None:
            self.output_dir_objectfiles = output_dir
        else:
            self.output_dir_objectfiles = output_dir_objectfiles


    @classmethod
    def use_config(cls, json_file):
        with open(json_file, 'r') as config_file:
            try:
                config_dict = json.load(config_file)
            except Exception as e:
                print(f"Error reading config file:{json_file}\n Error: {e}")

        try:
            return cls(
                command=config_dict[0]['command'],
                json_filename=config_dict[0]['json_filename'],
                log_file=config_dict[0]['log_file'],
                source_dir=config_dict[0]['source_dir'],
                output_dir=config_dict[0]['output_dir'],
                file_type=config_dict[0]['file_type'],
                lazy_load=config_dict[0]['lazy_load'],
                compile_dir_to_executable=config_dict[0]['compile_dir_to_executable']
            )

        except json.JSONDecodeError:
            print(f"Error: The file '{json_file}' is not a valid JSON file")

        except FileNotFoundError:
            print(f"Error: the file '{json_file}; was not found ")

        except Exception as e:
            print(f"An error occurred: {e}")

    def __compile_and_dump_exec_each(self, executeFlag=False, extra_run_args=None):
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
                                            os_type=self.os_type,
                                            extra_run_args=extra_run_args)

            compilation_results.append(result_of_compilation)

        json_file = os.path.join('./', self.json_filename)
        with open(json_file, 'w') as jsonFile:
            json.dump(compilation_results, jsonFile, indent=4)
        self._number_of_compiles += 1

        # logging logic
        log_to_file(json_file, self.log_file, self.lazy_load)

    def __compile_and_dump_exec_dir(self, executeFlag=False, extra_run_args=None, ExecName='a'):
        compilation_results = []
        extension = ''
        if self.os_type != "Windows":
            if ExecName == 'a':
                extension = '.out'

        extension = '.exe'  # will evaluate if we are on windows

        # lang_type is list
        files_to_compile = self.files_to_compile(filetype=self.file_type,
                                                 recursive_compile_dir=self.recursive_compile_dir)
        runcommands = [self.multi_command]

        # file append logic: logic for listing files to be compiled
        for file in files_to_compile:
            runcommands.append(os.path.join(self.source_dir, file))

        runcommands.append('-o')

        # the actual file being spat out
        output_binary = os.path.join(self.output_dir, ExecName)
        runcommands.append(output_binary)
        # end file append logic

        result_of_compilation = {
            'dir': [self.source_dir, ExecName + extension],
            'compile_status': '',
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
                                        output_bin=output_binary,
                                        extra_run_args=extra_run_args)

        compilation_results.append(result_of_compilation)

        json_file = os.path.join('./', self.json_filename)
        with open(json_file, 'w') as jsonFile:
            json.dump(compilation_results, jsonFile, indent=4)

        self._number_of_compiles += 1

        # logging logic
        log_to_file(json_file, self.log_file, self.lazy_load)

    def compile_and_dump_exec(self, compile_dir_to_executable: typing.Union[str, bool] = False, executeFlag=False,
                              extra_run_args=None):

        if compile_dir_to_executable:
            self.__compile_and_dump_exec_dir(executeFlag=executeFlag, ExecName=compile_dir_to_executable,
                                             extra_run_args=extra_run_args)

        else:
            self.__compile_and_dump_exec_each(executeFlag=executeFlag, extra_run_args=extra_run_args)

    def compile_to_obj_and_dump(self):
        # by default recursive_compile_dir should be used; not too important sha
        compilation_results = []
        extension = '.o'

        self.lazy_load_check_and_handle()  # handle lazy loading as usual

        # create all the object files, make them recursive if we are using recursive compile
        files_to_compile_list = self.files_to_compile(filetype=self.file_type,
                                                      recursive_compile_dir=self.recursive_compile_dir)

        # implement the commands

        for file in files_to_compile_list:
            commands: list = [self.command, '-c']
            file_parse = file.split('\\')
            commands.append(file)
            # very disgusting parsing lol
            object_file = (file_parse[len(file_parse) - 1]).split('.')[0] + extension
            commands.append('-o')
            commands.append(self.output_dir + object_file)
            result_of_compilation = {
                'name': [file, object_file],
                'compile_status': '',
                'output': '',
            }
            # execute is ALWAYS False and extra_run_args is ALWAYS None
            result_of_compilation = compile(runcommands=commands,
                                            execute=False,
                                            results=result_of_compilation,
                                            file_to_compile=file,
                                            output_bin=object_file,
                                            os_type=self.os_type,
                                            extra_run_args=None)

            compilation_results.append(result_of_compilation)

        json_file = os.path.join('./', self.json_filename)
        with open(json_file, 'w') as jsonFile:
            json.dump(compilation_results, jsonFile, indent=4)
        self._number_of_compiles += 1

        # logging logic
        log_to_file(json_file, self.log_file, self.lazy_load)