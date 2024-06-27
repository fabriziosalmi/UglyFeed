import subprocess
import streamlit as st

def run_script(script_name):
    """Execute a script and capture its output and errors."""
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
        return f"Script {script_name} execution failed.\n\n" \
               f"Status: {e.returncode}, Output: {e.stdout}, Errors: {e.stderr}"

def main():
    script_name = "script_runner.py"  # Replace with your script name
    output, errors = run_script(script_name)
    st.code(f"```\n{output}\n```")
    st.write(f"Errors:\n{errors}")

if __name__ == "__main__":
    main()
