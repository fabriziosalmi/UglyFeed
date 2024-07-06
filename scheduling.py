"""
Scheduling script for UglyFeed
"""

import time
from datetime import datetime
import threading
import logging
import schedule
from script_runner import run_script  # Import run_script to use for script execution

# Initialize the logger
logger = logging.getLogger(__name__)

class UglyFeedScheduler:
    """Class to encapsulate scheduling logic for UglyFeed."""

    def __init__(self):
        self.job_stats = []

    def run_scripts_sequentially(self, get_new_item_count, get_xml_item_count, st):
        """Run main.py, llm_processor.py, and json2rss.py sequentially and log their outputs."""
        scripts = ["main.py", "llm_processor.py", "json2rss.py"]
        item_count_before = get_xml_item_count() if get_xml_item_count else 0

        for script in scripts:
            try:
                if st:
                    with st.spinner(f"Executing {script}..."):
                        output, errors = run_script(script)
                        if st:
                            st.text_area(f"Output of {script}", output, height=200)
                else:
                    output, errors = run_script(script)

                logger.info("Output of %s:\n%s", script, output)
                if errors.strip() and errors != "No errors":
                    logger.error("Errors or logs of %s:\n%s", script, errors)
                    if st:
                        st.text_area(f"Errors of {script}", errors, height=200)

            except Exception as e:
                logger.error("Failed to execute %s: %s", script, e)
                self.job_stats.append({
                    'script': script,
                    'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'status': f'Failed with error: {e}',
                    'new_items': 0
                })
                continue  # Continue with the next script even if one fails

        new_items = get_new_item_count(item_count_before) if get_new_item_count else 0
        self.job_stats.append({
            'script': ', '.join(scripts),
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'Success' if new_items > 0 else 'No new items',
            'new_items': new_items
        })

    def schedule_jobs(self, interval, period, get_new_item_count=None, get_xml_item_count=None, st=None):
        """Schedule jobs to run periodically."""
        def job():
            try:
                self.run_scripts_sequentially(get_new_item_count, get_xml_item_count, st)
                self.job_stats.append({
                    'script': 'Scheduled Job',
                    'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'status': 'Success'
                })
            except Exception as e:
                self.job_stats.append({
                    'script': 'Scheduled Job',
                    'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'status': f'Failed with error: {e}'
                })
                logger.error("Scheduled job failed with error: %s", e)

        # Scheduling based on the specified period
        if period == 'minutes':
            schedule.every(interval).minutes.do(job)
        elif period == 'hours':
            schedule.every(interval).hours.do(job)
        elif period == 'days':
            schedule.every(interval).days.do(job)
        else:
            logger.error("Unsupported period: %s", period)
            return

        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_scheduling(self, interval, period, session_state, get_new_item_count=None, get_xml_item_count=None, st=None):
        """Start scheduling jobs if enabled in the config."""
        if session_state.config_data.get('scheduling_enabled', False):
            if interval <= 0:
                logger.error("Interval must be greater than 0")
                return
            if period not in ['minutes', 'hours', 'days']:
                logger.error("Invalid period specified. Must be 'minutes', 'hours', or 'days'.")
                return

            scheduling_thread = threading.Thread(
                target=self.schedule_jobs,
                args=(interval, period, get_new_item_count, get_xml_item_count, st),
                daemon=True
            )
            scheduling_thread.start()
            logger.info("Scheduling started with interval: %d %s", interval, period)
        else:
            logger.info("Scheduling is disabled in the configuration.")

# Backward compatibility global variable
job_stats_global = []

# Wrapper functions for backward compatibility
def run_scripts_sequentially(run_script, get_new_item_count, get_xml_item_count, logger, st):
    scheduler = UglyFeedScheduler()
    scheduler.run_scripts_sequentially(get_new_item_count, get_xml_item_count, st)
    # Append job stats to the global variable for backward compatibility
    global job_stats_global
    job_stats_global.extend(scheduler.job_stats)

def schedule_jobs(interval, period, get_new_item_count=None, get_xml_item_count=None, st=None):
    """Schedule jobs to run periodically."""
    scheduler = UglyFeedScheduler()
    scheduler.schedule_jobs(interval, period, get_new_item_count, get_xml_item_count, st)
    # Append job stats to the global variable for backward compatibility
    global job_stats_global
    job_stats_global.extend(scheduler.job_stats)

def start_scheduling(interval, period, session_state, get_new_item_count=None, get_xml_item_count=None, st=None):
    """Start scheduling jobs if enabled in the config."""
    scheduler = UglyFeedScheduler()
    scheduler.start_scheduling(interval, period, session_state, get_new_item_count, get_xml_item_count, st)
