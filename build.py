import platform
import os
import json
import typing
from utils.powerutils import lazy_load_func
from utils.powerutils import execute_commands
from utils.logging import log_to_file
# redundant lol
from main import cc_command


# please if you are reading this code to understand, start from here and the function compile_and_dump_exec
class BuildMachine:
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
                output_list.extend(self.resolve_dir(absolute_i_path + '/', file_types))
        return output_list

    def is_filetype(self, filetype: list[str], file: str):
        for extension in filetype:
            if file.endswith(extension):
                return True
        return False

    def files_to_compile(self, filetype, recursive_compile_dir, include_object_files=False):
        extensions = []
        c_extensions = ['.c']
        cpp_extensions = ['.cpp', '.cxx']
        object_file_extensions = ['.o']

        if filetype == 'c':
            extensions.extend(c_extensions)
        elif filetype == 'c++':
            extensions.extend(cpp_extensions)

        if include_object_files:
            extensions.extend(object_file_extensions)

        if recursive_compile_dir:
            return self.resolve_dir(self.source_dir, extensions)
        else:
            return [f for f in os.listdir(self.source_dir) if self.is_filetype(extensions, f)]

    def __init__(self, command, result_file, log_file, source_dir, output_dir, file_type, lazy_load=False,
                 compile_dir_to_executable=False, recursive_compile_dir=False, output_dir_executables=None,
                 output_dir_objectfiles=None, linker_config: typing.Union[dict, None] = None):
        self.files = None
        self.command = command
        self.multi_command = cc_command
        self.json_filename = result_file
        self.linker_config = linker_config  # please specify this to use it
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
                result_file=config_dict[0]['result_file'],
                log_file=config_dict[0]['log_file'],
                source_dir=config_dict[0]['source_dir'],
                output_dir=config_dict[0]['output_dir'],
                file_type=config_dict[0]['file_type'],
                lazy_load=config_dict[0]['lazy_load'],
                compile_dir_to_executable=config_dict[0]['compile_dir_to_executable'],
                output_dir_objectfiles=config_dict[0]['output_dir'] + config_dict[0]['output_dir_objectfiles'],
                output_dir_executables=config_dict[0]['output_dir'] + config_dict[0]['output_dir_executables'],
                recursive_compile_dir=config_dict[0]['recursive_compile_dir'],
                project_name=config_dict[0]['project_name']
            )

        except json.JSONDecodeError:
            print(f"Error: The file '{json_file}' is not a valid JSON file")

        except FileNotFoundError:
            print(f"Error: the file '{json_file}; was not found ")

        except Exception as e:
            print(f"An error occurred: {e}")

    def __compile_and_dump_exec_each(self, executeFlag=False, extra_run_args=None):

        """
           This function compiles all the C/C++ files in a directory to a binary in a target directory.
           It also chooses to optionally execute with the executeFlag flag

        """

        compilation_results = []
        extension = ''
        if self.os_type == "Windows":
            extension = '.exe'

        # check if lazy load is active
        self.lazy_load_check_and_handle()

        # compilation process

        # self.files is filled in the function lazy_load_check_and_handle
        for source_file in self.files:
            bin_name_parse_list = source_file.split('/')
            bin_name_parse_list = bin_name_parse_list[len(bin_name_parse_list) - 1]

            output_binary = os.path.join(self.output_dir_executables, bin_name_parse_list.split('.')[0])
            runcommands = [self.command, source_file, '-o', output_binary]

            result_of_compilation = {
                'name': [source_file, bin_name_parse_list.split('.')[0] + extension],
                'compile_status': '',
                'output': '',
            }
            result_of_compilation = execute_commands(runcommands=runcommands,
                                            execute=executeFlag,
                                            results=result_of_compilation,
                                            file_to_compile=bin_name_parse_list,
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

    def __compile_and_dump_dir_to_exec(self, executeFlag=False, extra_run_args=None, ExecName='a',
                                       include_obj_files=False):
        compilation_results = []
        extension = ''
        if self.os_type != "Windows":
            if ExecName == 'a':
                extension = '.out'

        extension = '.exe'  # will evaluate if we are on windows

        # lang_type is list
        files_to_compile = self.files_to_compile(filetype=self.file_type,
                                                 recursive_compile_dir=self.recursive_compile_dir,
                                                 include_object_files=include_obj_files)
        runcommands = [self.multi_command]
        # file append logic: logic for listing files to be compiled
        for file in files_to_compile:
            runcommands.append(os.path.join(self.source_dir, file))

        runcommands.append('-o')

        # the actual file being spat out
        output_binary = os.path.join(self.output_dir_executables, ExecName)
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
        result_of_compilation = execute_commands(runcommands=runcommands,
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
                              extra_run_args=None, include_obj_files=False):

        if compile_dir_to_executable:
            self.__compile_and_dump_dir_to_exec(executeFlag=executeFlag, extra_run_args=extra_run_args,
                                                ExecName=compile_dir_to_executable, include_obj_files=include_obj_files)

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
        # Note: this files_to_compile function encapsulate the source dir
        # implement the commands

        for file in files_to_compile_list:
            commands: list = [self.command, '-c']
            file_parse = file.split('/')
            commands.append(file)
            # very disgusting parsing lol
            object_file = (file_parse[len(file_parse) - 1]).split('.')[0] + extension
            commands.append('-o')
            commands.append(self.output_dir_objectfiles + object_file)
            result_of_compilation = {
                'name': [file, object_file],
                'compile_status': '',
                'output': '',
            }
            # execute is ALWAYS False and extra_run_args is ALWAYS None
            result_of_compilation = execute_commands(runcommands=commands,
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

    # def link_to_dir(self, source_dir_of_object_files, ld_args: dict, target_dir_for_executable, ExecName='a', ):
        """
                ld_args = {
            "output": "output_file",            # Output file name (-o)
            "input_files": ["file1.o", "file2.o"],  # Input object files                                                                                       \n
            "library_paths": ["/usr/lib", "/usr/local/lib"],  # Library search paths (-L)       SPECIFIES THE NAME OF THE PATHS FOR FINDING THE LIBRARY FILES  \n
            "libraries": ["m", "c"],           # Libraries to link against (-l)                 SPECIFIES THE NAME OF THE LIBRARIES IN THE LIBRARY PATHS FORM: libname.so or libname.a  \n
            "entry": "main",                   # Entry point (-e)                               SPECIFIES AND ENTRY POINT OTHER THAN MAIN                      \n
            "script": "linker_script.ld",      # Linker script (-T)                             WARNING: DONT TOUCH THIS FLAG, TOO SENSITIVE                   \n
            "shared": False,                   # Create shared library (-shared)                CREATES A SHARED LIBRARY AND NOT A BINARY                      \n
            "static": False,                   # Force static linking (-static)                 LINKING A STATIC LIBRARY TO THE OUTPUT                         \n
            "debug": True,                     # Include debugging information (-g)             ADDS DEBUG INFORMATION                                         \n
            "relocatable": False,              # Generate relocatable output (-r)
            "strip_debug": False,              # Strip debugging symbols (-S)
            "nostdlib": False,                 # Do not use standard libraries (-nostdlib)
            "verbose": False                   # Verbose mode (-v)
        }  \n
        Extra Notes .a files are linked statically: copied into the file statically.
        .so files are linked dynamically: copied into the executable at runtime
        """
        pass
