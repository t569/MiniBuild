# This File is to contain all the linking logic used to link the object files
import json
import os
import platform
from utils.powerutils import execute_commands
import typing


def is_filetype(filetype: list[str], file: str):
    for extension in filetype:
        if file.endswith(extension):
            return True
    return False


def resolve_extension(os_type):
    if os_type.lower() == "windows":
        return '.exe'
    else:
        return '.out'


def files_to_link(object_files_dir):
    object_file_extensions = ['.o']
    return [f for f in os.listdir(object_files_dir) if is_filetype(object_file_extensions, f)]


class LinkerMachine:

    def __init__(self, ld_args_json_config):
        self.os_type = platform.system()
        self.extension = resolve_extension(self.os_type)

        """
                    general ld args = {
                    "output": "output_file",            # Output file name (-o)
                    "input_files": ["file1.o", "file2.o"],  # Input object files                                                                                       \n
                    "library_paths": ["/usr/lib", "/usr/local/lib"],  # Library search paths (-L)       SPECIFIES THE NAME OF THE PATHS FOR FINDING THE LIBRARY FILES  \n
                    "libraries": ["m", "c"],           # Libraries to link against (-l)                 SPECIFIES THE NAME OF THE LIBRARIES IN THE LIBRARY PATHS FORM: libname.so or libname.a  \n
                    "entry": "main",                   # Entry point (-e)                               SPECIFIES AND ENTRY POINT OTHER THAN MAIN                      \n
                    "script": "linker_script.ld",      # Linker script (-T)                             WARNING: DONT TOUCH THIS FLAG, TOO SENSITIVE                   \n
                    "shared": False,                   # Create shared library (-shared)                CREATES A SHARED LIBRARY AND NOT A BINARY                      \n
                    "static": False,                   # Force static linking (-static)                 LINKING A STATIC LIBRARY TO THE OUTPUT                         \n
                    "debug": True,                     # Include debugging information (-g)             ADDS DEBUG INFORMATION                                         \n
                    "relocatable": False,              # Generate relocatable output (-r)               CREATES A RELOCATED OBJECT FILE FOR FURTHER                    \n
                    "strip_debug": False,              # Strip debugging symbols (-S)                   STRIPS DEBUG INFORMATION FROM THE OUTPUT opposite of (-g)      \n
                    "nostdlib": False,                 # Do not use standard libraries (-nostdlib)      STANDARD LIBRARY WILL REMOVE ANY STANDARD LIBRARY FILES IF THEY ARE NEEDED THEY WILL BE EXPLICITLY LINKED
                    "verbose": False                   # Verbose mode (-v)                              VERBOSE MODE GIVES YOU DETAILED INFO ON WHAT THE LINKER IS DOING
                }  \n
                Extra Notes:: .a files are linked statically: copied into the file statically.
                .so files are linked dynamically: copied into the executable at runtime

                Use ld_args to create the following: (we can ignore some flags like -e -T -
                build_configs = {
                "debug":{
                "ldflags": "-g",
                "output_dir":"build/debug",
                }
                "release":{
                "ldflags":"-s",
                "output_dir": "build/release",
                }

                object_files = input files
                external_libs = {
                "paths": library_paths,
                "libs": libraries,
                "crt": crt_path,
                "ld_so": dynamic_linker_path
                }

        """
        with open(ld_args_json_config, 'r') as ld_args:
            config_info = json.load(ld_args)

            self.ld_args = config_info
            self.source_dir = self.ld_args[0]['object_files_dir']
            self.build_type = self.ld_args[0]['build_type']
            self.ld_flag = self.ld_args[0]['ldflags'][self.build_type]
            self.lang_type = self.ld_args[0]['language']
            self.command = self.ld_args[0]['command']
            self.results = self.ld_args[0]['results']
            self.project_name = self.ld_args[0]['project_name']
            print(self.project_name)
            if self.lang_type is None:  # this is the default
                self.lang_type = "c"

            if self.command is None:  # This is the default
                self.lang_type = "gcc"

        # checking if the ld_args are actually
        # Omo let me chill here first

    def link_dir_to_exec(self, output_dir_param='./target/Executables/', project_name='test',
                         executeFlag=False, extra_run_args=None):  # this is the default

        object_files = files_to_link(self.source_dir)
        linking_results = []

        for iterator in range(len(object_files)):
            object_files[iterator] = os.path.join(self.source_dir, object_files[iterator])

        external_libraries = self.ld_args[0]['external_libraries']
        executable_name = self.ld_args[0]['executable_name']
        if executable_name is None:
            executable_name = 'a' + self.extension
        else:
            if self.os_type != "windows":
                # do nothing
                pass

        lib_paths_flags = [f"-L\"{path}\"" for path in external_libraries['paths']]
        lib_flags = [f"-l{lib}" for lib in external_libraries['libs']]

        build_type = self.ld_args[0]['build_type']
        output_dir = output_dir_param + project_name + '/' + 'build/' + build_type
        print(output_dir)

        # make the output build directory if it doesn't exist
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory: {output_dir} \n Error: {e} ")

        output_binary = os.path.join(output_dir + '/', executable_name)

        commands = [self.command, self.ld_flag, "-o", output_binary]

        commands.extend(object_files)
        if lib_paths_flags:
            commands.extend(lib_paths_flags)
            commands.extend(lib_flags)

        elif lib_flags:
            raise Exception("lib paths not specified")

        result_of_linking = {
            'dir': [self.project_name, executable_name],
            'link_status': '',
            'output': '',
        }
        print(commands)
        result_of_compilation = execute_commands(runcommands=commands,
                                                 execute=executeFlag,
                                                 file_to_compile=self.source_dir,
                                                 os_type=self.os_type,
                                                 results=result_of_linking,
                                                 output_bin=output_binary,
                                                 extra_run_args=extra_run_args)

        print("++++++++++++++++++++")
        print(result_of_compilation)

        linking_results.append(result_of_compilation)

        json_file = os.path.join('./', self.results)
        with open(json_file, 'w') as jsonFile:
            json.dump(linking_results, jsonFile, indent=4)


linker = LinkerMachine('linkerconfig.json')
linker.link_dir_to_exec()
