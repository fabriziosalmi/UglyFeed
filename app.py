import subprocess
import yaml
import logging
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("uglyfeed.log"),
    logging.StreamHandler()
])

def update_config(config_file, updates):
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        config.update(updates)

        with open(config_file, 'w') as file:
            yaml.safe_dump(config, file)
        
        logging.info(f"Config updated with {updates}")
    except Exception as e:
        logging.error(f"Failed to update config: {e}")
        sys.exit(1)

def read_feeds(feeds_file):
    try:
        with open(feeds_file, 'r') as file:
            feeds = file.readlines()
        return [feed.strip() for feed in feeds]
    except Exception as e:
        logging.error(f"Failed to read feeds file: {e}")
        sys.exit(1)

def execute_script(script):
    try:
        result = subprocess.run(['python', script], capture_output=True, text=True, check=True)
        logging.info(f"Executing {script}:\n{'='*80}\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Errors in {script}:\n{'='*80}\n{e.stderr}")
        raise
    except Exception as e:
        logging.error(f"Failed to execute {script}: {e}")
        raise

def main():
    config_file = 'config.yaml'
    feeds_file = 'input/feeds.txt'
    scripts = ['main.py', 'llm_processor.py', 'json2rss.py', 'serve.py']
    
    config_updates = {
        'log': {
            'level': 'DEBUG',
        },
        'fetch': {
            'timeout': 20,
        }
    }

    # Validate config file exists
    if not Path(config_file).is_file():
        logging.error(f"Config file not found: {config_file}")
        sys.exit(1)

    # Validate feeds file exists
    if not Path(feeds_file).is_file():
        logging.error(f"Feeds file not found: {feeds_file}")
        sys.exit(1)

    # Update the config file
    update_config(config_file, config_updates)

    # Read feeds from input/feeds.txt
    feeds = read_feeds(feeds_file)
    logging.info(f"Feeds: {feeds}")

    # Execute the scripts in order
    for script in scripts:
        try:
            execute_script(script)
        except Exception as e:
            logging.error(f"Execution halted due to error in {script}: {e}")
            break

if __name__ == "__main__":
    main()