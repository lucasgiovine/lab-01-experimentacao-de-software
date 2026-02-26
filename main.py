import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

def get_popular_repos(num_repos):
    pass

def get_repo_details(owner, repo):
    pass

def get_pull_requests(owner, repo):
    pass

def get_releases(owner, repo):
    pass

def get_closed_issues(owner, repo):
    pass

def collect_and_print_repo_info(repos):
    pass

if __name__ == "__main__":
    num_repos = 1000
    try: 
        repos = get_popular_repos(num_repos)
        collect_and_print_repo_info(repos)
    except Exception as e:
        print(e)