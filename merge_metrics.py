import json
import os
from glob import glob

# Function to read JSON file
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Directory containing the JSON files
directory = 'rewritten/'

# Read the content JSON file
content_file = glob(os.path.join(directory, '*_rewritten.json'))[0]
content_data = read_json(content_file)

# Extract the base name for the output file
base_name = os.path.basename(content_file).replace('_rewritten.json', '')

# Initialize variables to store metrics and aggregated scores
metrics = {}
aggregated_scores = {}

# Read all metric JSON files
for metric_file in glob(os.path.join(directory, '*_metrics_*.json')):
    metric_data = read_json(metric_file)
    
    # Extract metrics and aggregated scores
    for key, value in metric_data.items():
        if key.startswith("Aggregated"):
            aggregated_scores[key] = value
        else:
            metrics[key] = value

# Calculate the overall score as the average of all aggregated scores
if aggregated_scores:
    overall_score = sum(aggregated_scores.values()) / len(aggregated_scores)
else:
    overall_score = 0

# Include aggregated scores in metrics
metrics.update(aggregated_scores)
metrics["Overall Score"] = round(overall_score, 2)  # Round to 2 decimal places

# Create the final combined JSON structure
combined_json = {
    "source": {
        "title": content_data["title"],
        "content": content_data["content"],
        "processed_at": content_data["processed_at"],
        "links": content_data["links"]
    },
    "metrics": metrics
}

# Generate the output filename
output_file = os.path.join(directory, f'{base_name}_combined_metrics.json')

# Save the combined JSON to a new file
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(combined_json, file, ensure_ascii=False, indent=4)

print(f'Combined JSON file created: {output_file}')
