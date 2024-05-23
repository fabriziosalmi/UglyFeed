import os
import json
import glob
import subprocess
import logging
import re

# Suppress NLTK log messages
nltk_logger = logging.getLogger('nltk')
nltk_logger.setLevel(logging.ERROR)

# Set up logging for the script
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the directory containing the rewritten JSON files
REWRITTEN_DIR = 'rewritten'

# Define the evaluation scripts
EVALUATION_SCRIPTS = [
    'evaluate_cohesion_concreteness.py',
    'evaluate_cohesion_information_density.py',
    'evaluate_frequency.py',
    'evaluate_information_density.py',
    'evaluate_lexical_metrics.py',
    'evaluate_lexical_syntactic_metrics.py',
    'evaluate_noun_verb_metrics.py',
    'evaluate_punctuation_function_words.py',
    'evaluate_statistical_metrics.py',
    'evaluate_structural_metrics.py'
]

def run_evaluation_scripts(input_file, all_aggregated_scores):
    """Run evaluation scripts on the given input file and extract aggregated scores."""
    base_name = os.path.basename(input_file).replace('.json', '')
    for script in EVALUATION_SCRIPTS:
        logger.info("Running %s on %s", script, input_file)
        result = subprocess.run(['python', script, input_file], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("Error running %s on %s", script, input_file)
            logger.error(result.stderr)
        else:
            logger.info(result.stdout)

        # Extract aggregated scores immediately after the script runs
        metric_file_pattern = os.path.join(REWRITTEN_DIR, f'{base_name}_metrics_{script.split("_")[1]}*.json')
        metric_files = glob.glob(metric_file_pattern)
        logger.debug("Pattern used for glob: %s", metric_file_pattern)
        logger.info("Generated metric files: %s", metric_files)

        for metric_file in metric_files:
            if os.path.exists(metric_file):
                logger.info("Processing metric file: %s", metric_file)
                with open(metric_file, 'r') as file:
                    data = json.load(file)
                    extracted_scores = extract_aggregated_scores(data)
                    logger.info("Extracted aggregated scores from %s: %s", metric_file, extracted_scores)
                    all_aggregated_scores.extend(extracted_scores)
            else:
                logger.warning("Metric file %s does not exist", metric_file)

def extract_aggregated_scores(data):
    """Extract aggregated scores from the given JSON data."""
    aggregated_scores = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                aggregated_scores.extend(extract_aggregated_scores(value))
            elif re.match(r'Aggregated.*Score', key) and isinstance(value, (int, float)):
                logger.info("Found aggregated score: %s -> %s", key, value)
                aggregated_scores.append((key, value))
    elif isinstance(data, list):
        for item in data:
            aggregated_scores.extend(extract_aggregated_scores(item))
    return aggregated_scores

def calculate_average_aggregated_score(aggregated_scores):
    """Calculate the average of the aggregated scores."""
    if aggregated_scores:
        scores = [score for _, score in aggregated_scores]
        logger.debug("Calculating average of aggregated scores: %s", scores)
        return sum(scores) / len(scores)
    logger.debug("No aggregated scores found")
    return None

def merge_metrics_files(input_file, all_aggregated_scores):
    """Merge metrics files for the given input JSON file."""
    base_name = os.path.basename(input_file).replace('.json', '')
    pattern = os.path.join(REWRITTEN_DIR, f'{base_name}_metrics_*.json')

    merged_metrics = {}

    for file_path in glob.glob(pattern):
        logger.info("Processing metrics file: %s", file_path)
        with open(file_path, 'r') as file:
            data = json.load(file)
            logger.debug("Loaded data: %s", json.dumps(data, indent=2))

            for key, value in data.items():
                if key not in merged_metrics:
                    merged_metrics[key] = value
                else:
                    if isinstance(value, dict) and isinstance(merged_metrics[key], dict):
                        merged_metrics[key].update(value)
                    else:
                        if not isinstance(merged_metrics[key], list):
                            merged_metrics[key] = [merged_metrics[key]]
                        merged_metrics[key].append(value)

    logger.info("All aggregated scores: %s", all_aggregated_scores)
    overall_average_aggregated_score = calculate_average_aggregated_score(all_aggregated_scores)
    logger.info("Overall average aggregated score: %s", overall_average_aggregated_score)

    # Add all aggregated raw scores to the merged metrics
    for key, score in all_aggregated_scores:
        merged_metrics[key] = score

    merged_metrics['Overall Average Aggregated Score'] = overall_average_aggregated_score

    output_file_name = f"{base_name}_metrics_merged.json"
    output_file_path = os.path.join(REWRITTEN_DIR, output_file_name)

    with open(output_file_path, 'w') as output_file:
        json.dump(merged_metrics, output_file, indent=4)

    logger.info("Merged metrics written to %s", output_file_path)

def main():
    """Main script execution."""
    input_files = glob.glob(os.path.join(REWRITTEN_DIR, '*_rewritten.json'))

    if not input_files:
        logger.warning("No input files found.")
        return

    for input_file in input_files:
        logger.info("Processing input file: %s", input_file)
        all_aggregated_scores = []
        run_evaluation_scripts(input_file, all_aggregated_scores)
        merge_metrics_files(input_file, all_aggregated_scores)

if __name__ == '__main__':
    main()
