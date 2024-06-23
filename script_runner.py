import subprocess
import streamlit as st

def run_script(script_name):
    """Execute a script and capture its output and errors."""
    st.write(f"Running {script_name}...")
    try:
        process = subprocess.run(
            ["python", script_name],
            capture_output=True, text=True, check=True
        )
        output = process.stdout.strip() if process.stdout else "No output"
        errors = process.stderr.strip() if process.stderr else "No errors"
        return output, errors
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr
