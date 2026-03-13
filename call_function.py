from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from config import *


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


schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="reads/returns the content of a specific file",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file to write, relative to the working directory",
                ),
            },
            required=["file_path"],
        ),
    )

schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="executes a Python file and returns its output",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file to write, relative to the working directory",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(type=types.Type.STRING),
                    description="Optional list of arguments to pass to the script",
                ),
            },
            required=["file_path"],
        ),
    )

schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="writes text content to a file (overwriting if it exists)",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file to write, relative to the working directory",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The text to write into the target file",
                ),
            },
             required=["file_path", "content"],
        ),
    )

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file,schema_write_file]
)

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
    }

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool", 
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={
                        "error": f"Unknown function: {function_name}"
                        }
                        )
                    ]
                )

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
            )
        ],
    )

