# Introduction

This is a basic build system for C and C++ using python

There is a need for config to get the system to work

# Config
For the basic create a .env file in the build directory after pulling the repo and specify the following:
```
C_COMMAND = gcc
CPP_COMMAND = g++
CC_COMMAND = cc

OUTPUT_DIR = .\\target\\
SOURCE_DIR = .\\src\\
JsonFileName = results.json
LogDataBase = log.json
```

You can replace the various commands and paths with custom paths and files in the system

### Note:
**Remember to create the files and directories in case of errors**
(i haven't dealt with this yet)
## Config: Venv

you can install the venv as you please
## Config : Load Your variables
Create a main script and add the following:
```python

from dotenv import dotenv_values

import compile
from utils import readfiles

config = dotenv_values('./.env')

c_command = config['C_COMMAND']
cpp_command = config['CPP_COMMAND']
cc_command = config['CC_COMMAND']
output_dir = config['OUTPUT_DIR']
source_dir = config['SOURCE_DIR']
json_filename = config['ResultJsonFile']
log_file = config['LogDataBase']
```



# Build Setup: 
## Quick and Dirty

in the main script add the following:
```python

if __name__ == "__main__":
    my_first_machine = compile.CompileMachine(cpp_command, json_filename,
                                              log_file,  source_dir,
                                              output_dir, file_type='c++')
    my_first_machine.compile_and_dump_exec()
```
## Use a Build Config File
To use a custom JSON build config file first create the JSON file

```JSON
[
  {
    "command": "gcc",
    "json_filename": "results.json",
    "log_file": "log.json",
    "source_dir": ".\\src\\",
    "output_dir": ".\\target\\",
    "file_type": "c",
    "lazy_load": true,
    "compile_dir_to_executable": true
  }
]
```
Note that this has the same effect as if we used the .env file.
Choose as you please

Now call all of this in the main function using the following:
```python
my_first_machine.use_config(path_to_json_file)
```


# Execution
To modify the file and allow execution of the compiled code, change the last line to the following:
```python
my_first_machine.compile_and_dump_exec(executeFlag=True)
```


