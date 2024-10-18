import os
import json
import subprocess
from . import executefiles


# we need to define a class

# this will solve the problem of calling lazy_load on the first execution pipeline

# this function is used to change attributes of the class
def change_attribute(instance, attribute, new_value):
    if hasattr(instance, attribute):
        setattr(instance, attribute, new_value)
    else:
        raise ValueError(f'type: {type(instance)} has no attribute: {attribute}')


def changes_attributes(instance, attributes: dict):
    for old_attr, new_attr in attributes:
        setattr(instance, old_attr, new_attr)


def lazy_load_func(json_filename) -> list:
    json_file = os.path.join('./', json_filename)
    lazy_load_log = []
    with open(json_file, 'r') as jsonFile:  # read all things that have errors and put them in a list
        intermediate = json.load(jsonFile)

        for elem in intermediate:
            if elem['compile_status'] == 'failure':
                lazy_load_log.append(elem['name'][0])
    return lazy_load_log


def compile(runcommands, execute, results, file_to_compile, output_bin, os_type, extra_run_args=None) -> list:
    try:
        subprocess.run(runcommands, capture_output=True, text=True, check=True)

        print(f"Compilation of {file_to_compile} successful")
        results['compile_status'] = 'success'

        # output_bin = output_dir + file

        if execute:
            print(f"Executing {output_bin}...")
            stdout, stderr = executefiles.execute(os_type, output_bin, extra_run_args)
            results['output'] = {"stdout": stdout, "stderr": stderr}

        else:
            results['output'] = ''

    except subprocess.CalledProcessError as e:
        print(f"Error during compilation of {file_to_compile}")
        results['compile_status'] = 'failure'

        # capture the error message; Error message of death!!!
        results['output'] = {"stdout": e.stdout,
                             "stderr": e.stderr}

    finally:
        return results


def link(runcommands, execute,files_to_link, output_bin, os_type):
    pass