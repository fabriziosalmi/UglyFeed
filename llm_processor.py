import json
import requests
import os
from pathlib import Path

def call_llm_api(combined_content):
    """ Sends combined content to the LLM API and receives a rewritten version. """
    url = "http://192.168.100.41:11434/api/chat"
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({
        "model": "llama3",
        "messages": [{"role": "user", "content": combined_content}],
        "stream": False
    })
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()['message']['content']
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None

def process_json_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON from {filepath}: {e}")
        return

    combined_content = "\nCrea un unico contenuto in lingua italian da tutte le informazioni contenute in [content] \n".join(f"[source {idx + 1}] {item['content']}" for idx, item in enumerate(json_data))
    print(f"Processing {filepath} - sending to LLM API...")
    rewritten_content = call_llm_api(combined_content)

    if rewritten_content:
        new_data = {
            'title': f"{json_data[0]['title']}",
            'content': f"{rewritten_content}"
        }
        new_filename = Path('rewritten') / (Path(filepath).stem + '_rewritten.json')
        try:
            with open(new_filename, 'w', encoding='utf-8') as outfile:
                json.dump(new_data, outfile, indent=4)
            print(f"Rewritten file saved to {new_filename}")
        except IOError as e:
            print(f"Error writing to {new_filename}: {e}")
    else:
        print("Failed to get rewritten content from LLM API.")

def main():
    output_folder = Path('output')
    rewritten_folder = Path('rewritten')
    rewritten_folder.mkdir(parents=True, exist_ok=True)

    json_files = list(output_folder.glob('*.json'))
    if not json_files:
        print("No JSON files found in the output folder.")
        return

    for filepath in json_files:
        process_json_file(filepath)

if __name__ == "__main__":
    main()

