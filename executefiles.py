import os
import platform
import subprocess
import json


def execute(os_platform, executable_path,extra_args=None):

    if extra_args is None:
        extra_args = []
    if os_platform == "Windows":
        execute_result = subprocess.run([executable_path + '.exe'] + extra_args, capture_output=True, text=True, check=True)

    else:
        execute_result = subprocess.run(['./' + executable_path] + extra_args, capture_output=True, text=True, check=True)
    return execute_result.stdout, execute_result.stderr


def execute_and_dump(json_filename, bin_dir):
    # search through the json file
    json_file = os.path.join('./', json_filename)
    os_plat = platform.system()

    # execute them and put them in the json file
    extern_data = []
    with open(json_file, 'r+') as jsonFile:
        extern_data = json.load(jsonFile)

        for entry in extern_data:
            if entry.get('compile_status') == 'success' or entry.get('compile_link_status') == 'success':
                try:
                    executable_path = os.path.join(bin_dir, (entry.get('name')[1]).split('.')[0])
                    stdout, stderr = execute(os_plat, executable_path)
                    print(f"Execution of {executable_path} successful")
                    entry['output'] = {'stdout': stdout, 'stderr': stderr}

                except subprocess.CalledProcessError as e:
                    print(f"Error during execution of {executable_path}")
                    entry['output'] = {'runtime_error': e.returncode}

    with open(json_file, 'w+') as jsonFile:
        json.dump(extern_data, jsonFile, indent=4)










