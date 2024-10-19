# This File is to contain all the linking logic used to link the object files
import json
import build
import typing


class LinkerMachine:

    def __init__(self, ld_args_json_config):
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
                    "relocatable": False,              # Generate relocatable output (-r)               CREATES A RELOCATED OBJECT FILE FOR FURTHER                    \n
                    "strip_debug": False,              # Strip debugging symbols (-S)                   STRIPS DEBUG INFORMATION FROM THE OUTPUT opposite of (-g)      \n
                    "nostdlib": False,                 # Do not use standard libraries (-nostdlib)      STANDARD LIBRARY WILL REMOVE ANY STANDARD LIBRARY FILES IF THEY ARE NEEDED THEY WILL BE EXPLICITLY LINKED
                    "verbose": False                   # Verbose mode (-v)                              VERBOSE MODE GIVES YOU DETAILED INFO ON WHAT THE LINKER IS DOING
                }  \n
                Extra Notes:: .a files are linked statically: copied into the file statically.
                .so files are linked dynamically: copied into the executable at runtime

                Use ld_args to create the following:
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

            self.ld_args = config_info[0]['linker_config']
            print(self.ld_args)

        # checking if the ld_args are actually
        # Omo let me chill here first

linker = LinkerMachine()
