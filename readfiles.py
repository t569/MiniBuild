import platform
import subprocess
import os
import json
import executefiles

def lazy_load_func(json_filename) -> list:
    json_file = os.path.join('./', json_filename)
    lazy_load_log = []
    with open(json_file, 'r') as jsonFile:  # read all things that have errors and put them in a list
        intermediate = json.load(jsonFile)

        for elem in intermediate:
            if elem['compile_status'] == 'failure':
                lazy_load_log.append(elem['name'][0])
    return lazy_load_log


def compile_and_dump(command, json_filename, source_dir, output_dir, files, executeFlag=False, lazy_load=False):
    compilation_results = []
    extension = ''
    if platform.system() == "Windows":
        extension = '.exe'

    # check if lazy load is active
    if lazy_load:
        files = lazy_load_func(json_filename)
    # note: lazy load should be used only when recompiling as that is when it makes sense

    # compilation process
    for file in files:
        source_file = os.path.join(source_dir, file)
        output_binary = os.path.join(output_dir, file.split('.')[0])

        runcommands = [command, source_file, '-o', output_binary]

        result_of_compilation = {
            'name': [file, file.split('.')[0] + extension],
            'compile_status': '',
            'output': '',
        }
        try:
            result = subprocess.run(runcommands, capture_output=True, text=True, check=True)
            print(f"Compilation of {file} successful")
            result_of_compilation['compile_status'] = 'success'

            if executeFlag:
                print(f"Executing {output_binary}...")
                stdout, stderr = executefiles.execute(platform.system(), output_binary)
                result_of_compilation['output'] = {"stdout": stdout, "stderr": stderr}

            else:
                result_of_compilation['output'] = ''

        except subprocess.CalledProcessError as e:
            print(f"Error during compilation of {file}")
            result_of_compilation['compile_status'] = 'failure'

            result_of_compilation['output'] = {"stdout": e.stdout,
                                               "stderr": e.stderr}  # capture the error message; Error message of death!!!

        compilation_results.append(result_of_compilation)

    json_file = os.path.join('./', json_filename)
    with open(json_file, 'w') as jsonFile:
        json.dump(compilation_results, jsonFile, indent=4)


def helper_parse_lang_type(lang_type, f) -> bool:
    for _ in lang_type:
        if f.endswith('.' + _):
            return True

    return False


def compile_and_dump_dir(command, lang_type, json_filename, source_dir, output_dir, ExecName='a', executeFlag=False):
    compilation_results = []
    extension = ''
    if platform.system() != "Windows":
        if ExecName == 'a':
            extension = '.out'

    extension = '.exe'  # will evaluate if we are on windows

    # lang_type is list
    files_to_compile = [f for f in os.listdir(source_dir) if helper_parse_lang_type(lang_type, f)]

    runcommands = [command]
    for file in files_to_compile:
        runcommands.append(os.path.join(source_dir, file))

    runcommands.append('-o')
    output_binary = os.path.join(output_dir, ExecName)
    runcommands.append(output_binary)

    result_of_compilation = {
        'dir': [source_dir, ExecName + extension],
        'compile_link_status': '',
        'output': '',
    }

    try:
        subprocess.run(runcommands, capture_output=True, text=True, check=True)
        print(f"Compilation of {source_dir} successful")
        result_of_compilation['compile_link_status'] = 'success'

        if executeFlag:
            print(f"Executing {output_binary}...")
            stdout, stderr = executefiles.execute(platform.system(), output_binary)
            result_of_compilation['output'] = {"stdout": stdout, "stderr": stderr}

        else:
            result_of_compilation['output'] = ''

    except subprocess.CalledProcessError as e:
        print(f"Error during compilation of {source_dir}")
        result_of_compilation['compile_link_status'] = 'failure'

        result_of_compilation['output'] = {"stdout": e.stdout,
                                           "stderr": e.stderr}  # capture the error message; Error message of death!!!

    compilation_results.append(result_of_compilation)

    json_file = os.path.join('./', json_filename)
    with open(json_file, 'w') as jsonFile:
        json.dump(compilation_results, jsonFile, indent=4)
