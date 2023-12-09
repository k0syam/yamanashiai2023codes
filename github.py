import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import base64

load_dotenv()

github_token = os.getenv('GITHUB_TOKEN')
github_repo_owner = os.getenv('GITHUB_REPO_OWNER')
github_repo_name = os.getenv('GITHUB_REPO_NAME')

class GitHubUploader(object):

    def __init__(self) -> None:
        pass

    def upload_dir(self, dir_path, token=None, repo_owner=None, repo_name=None, branch='main'):
        files = []
        for root, _, filenames in os.walk(dir_path):
            for filename in filenames:
                files.append(os.path.join(root, filename))

        for file_path in files:
            print(f'Uploading {file_path}')
            self.upload_file(file_path, token, repo_owner, repo_name, branch)

    def upload_file(self, file_path, token=None, repo_owner=None, repo_name=None, branch='main'):
        if token == None:
            token = github_token
        if repo_owner == None:
            repo_owner = github_repo_owner
        if repo_name == None:
            repo_name = github_repo_name

        relative_path = os.path.relpath(file_path, os.getcwd())
        upload_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{relative_path}'

        with open(file_path, 'rb') as file:
            content = file.read()

        content_base64 = base64.b64encode(content).decode()

        headers = {
            'Authorization': f'token {token}',
            'Content-Type': 'application/json'
        }

        data = {
            'message': 'Upload file via API',
            'content': content_base64,
            'branch': branch
        }

        response = requests.put(upload_url, headers=headers, json=data)

        if response.status_code == 201:
            print(f'Successfully uploaded {relative_path} to {repo_owner}/{repo_name} on branch {branch}')
        else:
            print(f'Failed to upload {relative_path}. Status code: {response.status_code}, Message: {response.text}')

if __name__ == "__main__":
    github = GitHubUploader()
    github.upload_dir(dir_path='output/20231209_150836')