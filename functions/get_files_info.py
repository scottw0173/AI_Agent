import os
from google.genai import types

def get_files_info(working_directory, directory=".", verbose=False):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_target_dir = os.path.normpath(os.path.join(absolute_working_dir, directory))
    valid_target_dir = os.path.commonpath([absolute_working_dir, absolute_target_dir]) == absolute_working_dir

    lines = [f'Result for {directory} directory:']  # <-- MUST exist before appends

    if not valid_target_dir:
        msg = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        lines.append(msg)
        out = "\n".join(lines)
        if verbose:
            print(out)
        return out

    if not os.path.isdir(absolute_target_dir):
        msg = f'Error: {directory} is not a directory'
        lines.append(msg)
        out = "\n".join(lines)
        if verbose:
            print(out)
        return out

    list_of_files = os.listdir(absolute_target_dir)
    data_dictionary = {}
    for file in list_of_files:
        target_file = os.path.normpath(os.path.join(absolute_target_dir, file))
        data_dictionary[file] = f'file_size={os.path.getsize(target_file)}, is_dir={os.path.isdir(target_file)}'

    for file in data_dictionary:
        lines.append(f'-{file}: {data_dictionary[file]}')

    out = "\n".join(lines)
    if verbose:
        print(out)
    return out


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
