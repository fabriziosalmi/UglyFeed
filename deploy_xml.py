"""
This script uploads XML files to GitHub and GitLab repositories.
"""

import os
import base64
import logging
import requests
import yaml

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path='config.yaml'):
    """
    Load configuration from YAML or environment variables.
    """
    logging.info("Loading configuration from %s or environment variables...", config_path)
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    else:
        logging.warning("Configuration file %s not found. Falling back to environment variables.", config_path)
        config = {}

    config['github_token'] = config.get('github_token', os.getenv('GITHUB_TOKEN'))
    config['gitlab_token'] = config.get('gitlab_token', os.getenv('GITLAB_TOKEN'))
    config['github_repo'] = config.get('github_repo', os.getenv('GITHUB_REPO', 'user/uglyfeed'))
    config['gitlab_repo'] = config.get('gitlab_repo', os.getenv('GITLAB_REPO', 'user/uglyfeed'))
    config['enable_github'] = config.get('enable_github', str(os.getenv('ENABLE_GITHUB', 'true')).lower() == 'true')
    config['enable_gitlab'] = config.get('enable_gitlab', str(os.getenv('ENABLE_GITLAB', 'true')).lower() == 'true')

    return config

def upload_to_github(file_path, config):
    """
    Upload file to GitHub.
    """
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
    response = requests.get(url, headers=headers, timeout=10)
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
        logging.info("File %s exists in GitHub repo, updating it.", file_name)
    elif response.status_code == 404:
        # File does not exist, create it
        data = {
            'message': 'Add uglyfeed.xml',
            'content': content,
            'branch': 'main'
        }
        method = requests.put
        logging.info("File %s does not exist in GitHub repo, creating it.", file_name)
    else:
        logging.error("GitHub file check failed: %s", response.text)
        raise Exception(f"GitHub file check failed: {response.text}")

    # Upload or update the file
    response = method(url, json=data, headers=headers, timeout=10)
    if response.status_code in (200, 201):
        download_url = response.json()['content']['download_url']
        return download_url
    else:
        logging.error("GitHub upload failed: %s", response.text)
        raise Exception(f"GitHub upload failed: {response.text}")

def upload_to_gitlab(file_path, config):
    """
    Upload file to GitLab.
    """
    logging.info("Uploading to GitLab...")
    repo_name = config['gitlab_repo']
    token = config['gitlab_token']
    headers = {
        'PRIVATE-TOKEN': token
    }
    file_name = os.path.basename(file_path)
    url = f'https://gitlab.com/api/v4/projects/{repo_name}/repository/files/{file_name}'

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    data = {
        'branch': 'main',
        'content': content,
        'commit_message': 'Add uglyfeed.xml'
    }

    response = requests.post(url, json=data, headers=headers, timeout=10)
    if response.status_code == 201:
        download_url = f'https://gitlab.com/{repo_name}/-/raw/main/{file_name}'
        return download_url
    elif response.status_code == 400 and 'already exists' in response.text:
        # Update file if it already exists
        logging.info("File already exists on GitLab, attempting to update...")
        response = requests.put(url, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            download_url = f'https://gitlab.com/{repo_name}/-/raw/main/{file_name}'
            return download_url
        else:
            logging.error("GitLab update failed: %s", response.text)
            raise Exception(f"GitLab update failed: {response.text}")
    else:
        logging.error("GitLab upload failed: %s", response.text)
        raise Exception(f"GitLab upload failed: {response.text}")

def deploy_xml(file_path, config):
    """
    Deploy XML file to GitHub and GitLab based on the configuration.
    """
    urls = {}

    if config.get('enable_github', False):
        try:
            github_url = upload_to_github(file_path, config)
            urls['github'] = github_url
        except Exception as e:
            logging.error("GitHub upload error: %s", e)

    if config.get('enable_gitlab', False):
        try:
            gitlab_url = upload_to_gitlab(file_path, config)
            urls['gitlab'] = gitlab_url
        except Exception as e:
            logging.error("GitLab upload error: %s", e)

    return urls

if __name__ == '__main__':
    # Load configuration
    config = load_config()

    # File to deploy
    XML_FILE_PATH = 'uglyfeeds/uglyfeed.xml'

    # Deploy the XML file
    urls = deploy_xml(XML_FILE_PATH, config)

    # Print the URLs
    if urls:
        logging.info("File deployed to the following URLs:")
        for platform, url in urls.items():
            print(f"{platform.capitalize()}: {url}")
    else:
        logging.info("No deployments were made.")
