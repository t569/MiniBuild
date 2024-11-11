# Introduction

This is a basic build system for C and C++ using python

There is a need for config to get the system to work

# Config
For the basic create a .env file in the build directory after pulling the repo and specify the following:
```dotenv
C_COMMAND=gcc
CPP_COMMAND=g++
CC_COMMAND=cc

OUTPUT_DIR=./target/
EXECUTABLES_DIR=/ExecutableFiles/
OBJECTFILES_DIR=/ObjectFiles/
SOURCE_DIR=./src/
RESULT_JSON_FILE=logs/results.json
LOG_DATABASE=logs/log.json
```

You can replace the various commands and paths with custom paths and files in the system

### Note:
**Remember to create the files and directories in case of errors**
(i haven't dealt with this yet)

### Note:
there are stilla couple of parameters to be specified if you're using a .env like lazyLoad for example
## Config: Venv

you can install the venv as you please. If you are new to all this, then this section is for you

###  Windows

* If you do not have virtualenv go to the terminal and run the following:
```commandline
pip install virtualenv
```


#### To configure your venv, go to the directory of the project MiniBuild and run the following in a terminal in that directory:
```commandline
python -m venv myenvname
```

* Now navigate to the activate file to get the virtual environment up and running
```commandline
myenvname\Scripts\activate
```

### Linux
* To install on Linux, first check if pip is installed: 
```commandline
pip --version
```


* If it is not installed run the following command in the terminal:
#### Ubuntu : 
```commandline
sudo apt-get install python-pip
```

#### Arch Linux : 
```commandline
sudo pacman -S python-pip
```

#### Red Hat Linux (Fedora)
```commandline
sudo dnf install python3-pip
```
* After that, run the following:

```commandline
pip install virtualenv
```

* Now check your installation:
```commandline
virtualenv --version
```

#### Create the virtual environment by running the following command:

```commandline
virtualenv myenvname
```

* To activate the virtual environment run the following:
```commandline
source myenvname/bin/activate
```

* To deactivate run the following command:
```commandline
deactivate
```

### With the Virtual environment enabled, run the following commands:

#### Windows : 
```commandline
pip install requirements.txt
```

#### Linux : 
```commandline
pip3 install requirements.txt
```

**Note: For this to work, the virtual environment must be inside the MiniBuild directory**


## Config : Load Your variables
Create a main script and add the following:




```python
import os

from dotenv import dotenv_values

import build
import utils.executefiles
from utils import powerutils

config = dotenv_values('./.env')

c_command = config['C_COMMAND']
cpp_command = config['CPP_COMMAND']
cc_command = config['CC_COMMAND']
output_dir = config['OUTPUT_DIR']
output_dir_executables = config['OUTPUT_DIR'] + config['EXECUTABLES_DIR']
output_dir_object_files = config['OUTPUT_DIR'] + config['OBJECTFILES_DIR']
source_dir = config['SOURCE_DIR']
result_file = config['RESULT_JSON_FILE']
log_file = config['LOG_DATABASE']

```



# Build Setup: 
## Intro to Building: Quick and Dirty

in the main script add the following:
```python

if __name__ == "__main__":
    my_fourth_machine = build.CompileMachine(c_command, result_file, log_file, source_dir, output_dir, file_type='c')
    my_first_machine.compile_and_dump_exec()
```

One can specify a subdirectory in the output directory by appending the following to the file:
```python
powerutils.change_attribute(my_fourth_machine, 'output_dir_executables', output_dir_executables)
```
## Building: Use a Build Config File
To use a custom JSON build config file first create the JSON file

```JSON
[
  {
    "command": "gcc",
    "compile_dir_to_executable": true,
    "file_type": "c",
    "result_file": "logs/results.json",
    "lazy_load": true,
    "log_file": "logs/log.json",
    "output_dir": "./target/",
    "output_dir_executables": "Executables/",
    "output_dir_objectfiles": "ObjectFiles/",
    "recursive_compile_dir": false,
    "source_dir": "./src/"
  }
]
```
Note that this has the same effect as if we used the .env file.
Choose as you please

Now call all of this in the main function using the following:
```python
my_first_machine.use_config(path_to_json_file)
my_first_machine.compile_and_dump_exec()
```

## Build to Object Files: Building

One can also build to object files using the following (note this specifies a subdirectory in the target directory):
```python
 powerutils.change_attribute(my_fourth_machine, 'output_dir_objectfiles', output_dir_object_files)
    my_fourth_machine.compile_to_obj_and_dump()
```
## Build to Object Files: Linking
To build a dir of object files to an executable one has to invoke the linker machine. to do that one has to go through the following steps

### Create a linkerconfig json file
Create a file with any name of your choice (prefarably linkerconfig.json) and type the following:
```JSON
[
  {
    "build_type": "debug",
    "language": "c",
    "command": "gcc",
    "object_files_dir": "/target/ObjectFiles/",
    "output_exec_dir": "/target/Executables/",
    "external_libraries": {
      "paths": [],
      "libs": []
    },
    "results": "logs/results.json",
    "executable_name": "default",
    "ldflags": {
        "debug": "-g",
        "release": "-s"
      }
    }
]
```
change the attributes as needed. If they do not exist use the ```null``` keyword
### Modify main.py to run linker machine
Now open up main.py and add the following:
```python
import linker
...
...
my_linker = LinkerMachine(path_to_config)
my_linker.link_dir_to_exec(project_name='example',executeFlag=False) 
```
as usual change parameters asper specification

# Execution
To modify the file and allow execution of the compiled executable, change the last line to the following:
```python
my_first_machine.compile_and_dump_exec(executeFlag=True)
```

# The BIG IDEA: Create a Project Build Machine

To create a project build machine the steps are very straight forward:

## Import the project module into main.py:
```python
import project
```

## Create a linker config and build config json file:
* linkerconfig.json
```JSON
[
  {
    "build_type": "debug",
    "language": "c",
    "command": "gcc",
    "object_files_dir": "/target/ObjectFiles/",
    "output_exec_dir": "/target/Executables/",
    "external_libraries": {
      "paths": [],
      "libs": []
    },
    "results": "logs/results.json",
    "executable_name": "default",
    "ldflags": {
        "debug": "-g",
        "release": "-s"
      }
    }
]
```

* buildconfig.json
```JSON
[
  {
    "command": "gcc",
    "compile_dir_to_executable": true,
    "file_type": "c",
    "lazy_load": true,
    "log_file": "logs/log.json",
    "output_dir": "/target/",
    "output_dir_executables": "Executables/",
    "output_dir_objectfiles": "ObjectFiles/",
    "recursive_compile_dir": false,
    "result_file": "logs/results.json",
    "source_dir": "/src/"
  }
]
```
As usual, change asper specification

## Initialise a project machine in main.py

```python
myprj = Project('buildconfig.json','linkerconfig.json')
```

## Compile link and run pipeline
```python
myprj.compile_to_object_files()
myprj.link_to_executable()
myprj.run_executable(log_to_results=True)
```
** Note: the ```Project``` class initialises its own ```BuildMachine``` object and ```LinkerMachine``` object **

