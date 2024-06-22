import schedule
import time
from datetime import datetime
import threading

job_stats_global = []

def run_scripts_sequentially(run_script, get_new_item_count, get_xml_item_count, logger, st):
    """Run main.py, llm_processor.py, and json2rss.py sequentially and log their outputs."""
    scripts = ["main.py", "llm_processor.py", "json2rss.py"]
    item_count_before = get_xml_item_count()

    for script in scripts:
        with st.spinner(f"Executing {script}..."):
            output, errors = run_script(script)
            logger.info(f"Output of {script}:\n{output}")
            if errors.strip() and errors != "No errors":
                logger.error(f"Errors or logs of {script}:\n{errors}")

            st.text_area(f"Output of {script}", errors, height=200)

    new_items = get_new_item_count(item_count_before)
    job_stats_global.append({
        'script': ', '.join(scripts),
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'Success',
        'new_items': new_items
    })

def schedule_jobs(run_scripts_sequentially, interval, period, job_stats_global):
    """Schedule jobs to run periodically."""
    def job():
        run_scripts_sequentially()
        job_stats_global.append({
            'script': 'Scheduled Job',
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'Success'
        })

    if period == 'minutes':
        schedule.every(interval).minutes.do(job)
    elif period == 'hours':
        schedule.every(interval).hours.do(job)
    elif period == 'days':
        schedule.every(interval).days.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduling(interval, period, session_state):
    """Start scheduling jobs if enabled in the config."""
    if session_state.config_data.get('scheduling_enabled', False):
        scheduling_thread = threading.Thread(target=schedule_jobs, args=(interval, period), daemon=True)
        scheduling_thread.start()
