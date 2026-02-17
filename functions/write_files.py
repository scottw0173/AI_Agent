import os

def write_file(working_directory, file_path, content):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_file_path = os.path.normpath(os.path.join(absolute_working_dir, file_path))
    valid_target_file = os.path.commonpath([absolute_working_dir, absolute_file_path]) == absolute_working_dir
    if not valid_target_file:
        return print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    is_dir_check = os.path.isdir(absolute_file_path) #Returns True if file is invalid (if it is a directory instead of a file)
    if is_dir_check:
        return print(f'Error: Cannot write to "{file_path}" as it is a directory')
    try:
        os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)
    except FileExistsError:
        print(f"The file already exists")
        pass
    with open(absolute_file_path, 'w') as f:
        f.write(content)
    return print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')