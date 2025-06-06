import json
from colorama import Fore
from modules.utils import custom_serializer


def code_commit_init_enum(victim_code_commit_client, attacker_code_commit_client):
    list_repos(victim_code_commit_client)

def list_repos(code_commit_client):
    print(f"{Fore.GREEN}Enumerating Code Commit...")
    try:
        response = code_commit_client.list_repositories()
        repos = response.get("repositories", [])
        for repo in repos:
            print(f"{Fore.MAGENTA}Repository: {repo['repositoryName']} | ID: {repo['repositoryId']}")
            get_repo(code_commit_client, repo['repositoryName'])
            list_branches(code_commit_client, repo['repositoryName'])
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list code commits")

def get_repo(code_commit_client, repo_name):
    try:
        response = code_commit_client.get_repository(repositoryName=repo_name)
        metadata = response.get("repositoryMetadata", {})
        print(f"{Fore.YELLOW}{json.dumps(metadata, indent=4, sort_keys=True, default=custom_serializer)}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to get repository metadata for {repo_name}")

def list_branches(code_commit_client, repo_name):
    try:
        response = code_commit_client.list_branches(repositoryName=repo_name)
        branches = response.get("branches", {})
        print(f"{Fore.YELLOW}{repo_name} branches:\n{json.dumps(branches, indent=4, sort_keys=True, default=custom_serializer)}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to get repository branches for {repo_name}")