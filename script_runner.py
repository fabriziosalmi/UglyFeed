"""
Streamlit script runner for executing Python scripts and capturing their output and errors.
"""

import subprocess
import streamlit as st

def run_script(script_name: str) -> tuple[str, str]:
    """
    Execute a script and capture its output and errors.

    Args:
        script_name (str): The name of the script to execute.

    Returns:
        tuple: A tuple containing the script output and errors.
    """
    st.write(f"Running {script_name}...")
    try:
        process = subprocess.run(
            ["python", script_name],
            capture_output=True, text=True, timeout=60
        )
        output = process.stdout.strip() if process.stdout else "No output"
        errors = process.stderr.strip() if process.stderr else "No errors"
        return output, errors
    except subprocess.CalledProcessError as e:
        return (f"Script {script_name} execution failed.\n\n"
                f"Status: {e.returncode}, Output: {e.stdout}, Errors: {e.stderr}"), "Errors"
    except subprocess.TimeoutExpired as e:
        return f"Script {script_name} execution timed out.\n\nErrors: {e.stderr}", "Errors"
    except Exception as e:
        return f"An unexpected error occurred while running {script_name}: {e}", "Errors"

def main():
    """
    Main function to run the specified script and display its output and errors.
    """
    script_name = "script_runner.py"  # Replace with your script name
    output, errors = run_script(script_name)
    st.code(f"```\n{output}\n```")
    st.write(f"Errors:\n{errors}")

if __name__ == "__main__":
    main()
