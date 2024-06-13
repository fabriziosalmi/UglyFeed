import os
import yaml
import requests
import base64
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to load configuration from YAML or environment variables
def load_config(config_path='config.yaml'):
    logging.info(f"Loading configuration from {config_path} or environment variables...")
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    else:
        logging.warning(f"Configuration file {config_path} not found. Falling back to environment variables.")
        config = {}

    config['github_token'] = config.get('github_token', os.getenv('GITHUB_TOKEN'))
    config['gitlab_token'] = config.get('gitlab_token', os.getenv('GITLAB_TOKEN'))
    config['github_repo'] = config.get('github_repo', os.getenv('GITHUB_REPO', 'user/uglyfeed'))
    config['gitlab_repo'] = config.get('gitlab_repo', os.getenv('GITLAB_REPO', 'user/uglyfeed'))
    config['enable_github'] = config.get('enable_github', str(os.getenv('ENABLE_GITHUB', 'true')).lower() == 'true')
    config['enable_gitlab'] = config.get('enable_gitlab', str(os.getenv('ENABLE_GITLAB', 'true')).lower() == 'true')

    return config

# Function to upload file to GitHub
def upload_to_github(file_path, config):
    logging.info("Uploading to GitHub...")
    repo_name = config['github_repo']
    token = config['github_token']
    file_name = os.path.basename(file_path)
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{repo_name}/contents/{file_name}'

    # Read the file content
    with open(file_path, 'rb') as file:
        content = base64.b64encode(file.read()).decode('utf-8')

    # Check if the file exists in the repository
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # File exists, retrieve its SHA
        sha = response.json()['sha']
        data = {
            'message': 'Update uglyfeed.xml',
            'content': content,
            'sha': sha,
            'branch': 'main'
        }
        method = requests.put
        logging.info(f"File {file_name} exists in GitHub repo, updating it.")
    elif response.status_code == 404:
        # File does not exist, create it
        data = {
            'message': 'Add uglyfeed.xml',
            'content': content,
            'branch': 'main'
        }
        method = requests.put
        logging.info(f"File {file_name} does not exist in GitHub repo, creating it.")
    else:
        logging.error(f"GitHub file check failed: {response.text}")
        raise Exception(f"GitHub file check failed: {response.text}")

    # Upload or update the file
    response = method(url, json=data, headers=headers)
    if response.status_code in (200, 201):
        download_url = response.json()['content']['download_url']
        return download_url
    else:
        logging.error(f"GitHub upload failed: {response.text}")
        raise Exception(f"GitHub upload failed: {response.text}")

# Function to upload file to GitLab
def upload_to_gitlab(file_path, config):
    logging.info("Uploading to GitLab...")
    repo_name = config['gitlab_repo']
    token = config['gitlab_token']
    headers = {
        'PRIVATE-TOKEN': token
    }
    file_name = os.path.basename(file_path)
    url = f'https://gitlab.com/api/v4/projects/{repo_name}/repository/files/{file_name}'

    with open(file_path, 'r') as file:
        content = file.read()

    data = {
        'branch': 'main',
        'content': content,
        'commit_message': 'Add uglyfeed.xml'
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        download_url = f'https://gitlab.com/{repo_name}/-/raw/main/{file_name}'
        return download_url
    elif response.status_code == 400 and 'already exists' in response.text:
        # Update file if it already exists
        logging.info("File already exists on GitLab, attempting to update...")
        response = requests.put(url, json=data, headers=headers)
        if response.status_code == 200:
            download_url = f'https://gitlab.com/{repo_name}/-/raw/main/{file_name}'
            return download_url
        else:
            logging.error(f"GitLab update failed: {response.text}")
            raise Exception(f"GitLab update failed: {response.text}")
    else:
        logging.error(f"GitLab upload failed: {response.text}")
        raise Exception(f"GitLab upload failed: {response.text}")

# Main function to deploy XML file
def deploy_xml(file_path, config):
    urls = {}

    if config.get('enable_github', False):
        try:
            github_url = upload_to_github(file_path, config)
            urls['github'] = github_url
        except Exception as e:
            logging.error(f"GitHub upload error: {e}")

    if config.get('enable_gitlab', False):
        try:
            gitlab_url = upload_to_gitlab(file_path, config)
            urls['gitlab'] = gitlab_url
        except Exception as e:
            logging.error(f"GitLab upload error: {e}")

    return urls

if __name__ == '__main__':
    # Load configuration
    config = load_config()

    # File to deploy
    xml_file_path = 'uglyfeeds/uglyfeed.xml'

    # Deploy the XML file
    urls = deploy_xml(xml_file_path, config)

    # Print the URLs
    if urls:
        logging.info("File deployed to the following URLs:")
        for platform, url in urls.items():
            print(f"{platform.capitalize()}: {url}")
    else:
        logging.info("No deployments were made.")
