# uglypy/cli.py
import subprocess
import os
import argparse
from logging_setup import setup_logging, get_logger

# Setup logging
logger = setup_logging()

def run_command(command):
    """Run a command with subprocess and log the outcome."""
    logger.info(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        logger.info(f"Command {' '.join(command)} executed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Command {' '.join(command)} failed: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def run_streamlit(extra_args):
    """Run the Streamlit application."""
    command = ["streamlit", "run", "gui.py"] + extra_args
    run_command(command)

def run_script(script_name, extra_args):
    """Run the specified Python script with additional arguments."""
    script_path = os.path.join(os.getcwd(), script_name)

    if not os.path.isfile(script_path):
        logger.error(f"Error: {script_name} not found.")
        return

    command = ["python", script_path] + extra_args
    run_command(command)

def display_help():
    """Display help information with examples."""
    help_text = """
    uglypy - Command-line interface for running various scripts.

    Usage:
        uglypy <script> [script_args]

    Scripts:
        gui              Run the Streamlit GUI application.
        main             Run the main processing script.
        llm_processor    Run the LLM processor script.
        json2rss         Run the JSON to RSS converter script.
        deploy_xml       Run the XML deployment script.

    Examples:
        uglypy gui --server.address 0.0.0.0
        uglypy main --some-arg value
        uglypy llm_processor --another-arg value
        uglypy json2rss --yet-another-arg value
        uglypy deploy_xml --arg value

    For more information, visit the documentation at https://github.com/fabriziosalmi/UglyFeed
    """
    print(help_text)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="uglypy command-line interface", add_help=False)
    parser.add_argument("script", type=str, help="Script to run (e.g., gui, main, llm_processor, json2rss, deploy_xml, help)")
    parser.add_argument('script_args', nargs=argparse.REMAINDER, help="Arguments to pass to the script")
    return parser.parse_args()

def main():
    """Parse arguments and run the appropriate script."""
    args = parse_arguments()

    if args.script == "help":
        display_help()
    elif args.script == "gui":
        run_streamlit(args.script_args)
    else:
        run_script(f"{args.script}.py", args.script_args)

if __name__ == "__main__":
    main()
