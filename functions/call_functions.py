from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_files import schema_write_files, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_files,
        schema_run_python_file,
    ]
)

def call_function(function_calls,verbose=False):
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_files": write_file,
        "run_python_file": run_python_file,
    }

    parts = []

    for call in function_calls:
        function_name = call.name or ""
        print(f" - Calling function: {function_name}")  # KEEP: tests want this

        args = dict(call.args) if call.args else {}
        args["working_directory"] = "."          # sandbox root you control
        args["verbose"] = verbose               # you control, not the model

        result = function_map[function_name](**args)

        try:
            result = function_map[function_name](**args)
            parts.append(
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result},
                )
            )
        except Exception as e:
            parts.append(
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e), "received_args": args},
                )
            )

    return parts
