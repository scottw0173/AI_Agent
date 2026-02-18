import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None, verbose=False):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_file_path = os.path.normpath(os.path.join(absolute_working_dir, file_path))
    valid_target_file = os.path.commonpath([absolute_working_dir, absolute_file_path]) == absolute_working_dir
    if not valid_target_file:
        return print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(absolute_file_path):
        return print(f'Error: "{file_path}" does not exist or is not a regular file')
    if not file_path.strip().endswith('.py'):
        return print(f'Error: "{file_path}" is not a Python file')
    command = ["python", absolute_file_path]
    if args != None:
        for arg in args:
            command.extend(arg)
    first_process = subprocess.run(command, capture_output=True, cwd= absolute_working_dir, timeout=30, text=True)
    output_string = ""
    if first_process.returncode != 0:
        output_string += f'Process exited with code {first_process.returncode}'
    if first_process.stdout == None or first_process.stderr == None:
        output_string += "No output produced"
    else:
        output_string += f' Commands: {first_process.args} \n STDOUT: {first_process.stdout} \n STDERR: {first_process.stderr}'
        return print(output_string)
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Allows the user to design a series of commands to be ran in a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to python file that we wish to run commands. Should be relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A potential array of argument strings that will be applied to the command list before running",
            ),
        },
        required=["file_path"],
    ),
)