import platform
import subprocess
import os
import json
import executefiles


def compile_and_dump(command, json_filename, source_dir, output_dir, files, executeFlag=False):
    compilation_results = []
    extension = ''
    if platform.system() == "Windows":
        extension = '.exe'

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
                result_of_compilation['output'] = executefiles.execute(platform.system(), output_binary)

            else:
                result_of_compilation['output'] = ''

        except subprocess.CalledProcessError as e:
            print(f"Error during compilation of {file}")
            result_of_compilation['compile_status'] = 'failure'
            result_of_compilation['output'] = e.stderr  # capture the error message

        compilation_results.append(result_of_compilation)

    json_file = os.path.join('./', json_filename)
    with open(json_file, 'w') as jsonFile:
        json.dump(compilation_results, jsonFile, indent=4)
