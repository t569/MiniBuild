import os
import platform
import subprocess
import json


def execute(os_platform, executable_path):
    if os_platform == "Windows":
        execute_result = subprocess.run([executable_path + '.exe'], capture_output=True, text=True, check=True)

    else:
        execute_result = subprocess.run(['./' + executable_path], capture_output=True, text=True, check=True)

    return execute_result.stdout


def execute_and_dump(json_filename, bin_dir,):
    # search through the json file
    json_file = os.path.join('./', json_filename)
    os_plat = platform.system()

    # execute them and put them in the json file
    extern_data = []
    with open(json_file, 'r+') as jsonFile:
        extern_data = json.load(jsonFile)

        for entry in extern_data:
            executable_path = os.path.join(bin_dir, (entry.get('name')[1]).split('.')[0])
            entry['output'] = execute(os_plat, executable_path)

    with open(json_file, 'w+') as jsonFile:
        json.dump(extern_data, jsonFile, indent=4)









