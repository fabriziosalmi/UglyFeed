import subprocess

def run_script(script_name):
    """Execute a script and capture its output and errors."""
    process = subprocess.run(["python", script_name], capture_output=True, text=True)
    output = process.stdout.strip() if process.stdout else "No output"
    errors = process.stderr.strip() if process.stderr else "No errors"
    return output, errors
