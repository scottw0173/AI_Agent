import os
def get_file_content(working_directory, file_path):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_file_path = os.path.normpath(os.path.join(absolute_working_dir, file_path))
    valid_target_file = os.path.commonpath([absolute_working_dir, absolute_file_path]) == absolute_working_dir
    #print(f'HERE ARE RELEVANT VALUES:\n{absolute_working_dir}\n{absolute_file_path}\n{valid_target_file}')
    if not valid_target_file:
        return print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    is_file = os.path.isfile(absolute_file_path)
    if not is_file:
        return print(f'Error: File not found or is not a regular file: "{file_path}"')
    MAX_CHARS = 10000
    with open(absolute_file_path, 'r') as f:
        file_content_string = f.read(MAX_CHARS)
        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    print(file_content_string)

    
    return

