import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        wok_dir = os.path.dirname(target_file)

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        rest = subprocess.run(command,capture_output=True, cwd=working_dir_abs, timeout=30, text=True)
        what = ""
        if rest.returncode != 0:
            what += f"Process exited with code {rest.returncode}"
        if not rest.stdout and not rest.stderr:
            what +="No output produced"
        else:
            what += f"STDOUT:{rest.stdout}"
            what += f"STDERR:{rest.stderr}"
        return what
        
    except Exception as Error:
        return f"Error: executing Python file: {Error}"
