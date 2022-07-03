import imp
from django.conf import settings

from .git_api import GithubRepo, GithubClient
from .tasks import save_requirements_task

def get_url_from_repo(repo_name):
    token = getattr(settings, 'GITHUB_TOKEN', '')
    gh = GithubClient(token)
    url = gh.fetch_repo_archive_url(repo_name)
    return url

def get_top_repos(top_n):
    """ Returns list of (repo_name, url) """
    top_repos = []
    token = getattr(settings, 'GITHUB_TOKEN', '')
    gh = GithubClient(token)
    names_list = gh.get_popular_repos(top_n, 'python')
    for repo_name in names_list:
        url = gh.fetch_repo_archive_url(repo_name)
        top_repos.append((repo_name, url))
    return top_repos

def create_requiremets_for_repo(repo_name):
    """
    This function calls a bg task that fetches all the requirements from the GitHub API
    and connects all requirements with the given repo name
    
    Important! Any Real-Time calls that shouldn't wait for the backend should be called here
    
    Args:
        repo_name: obvius
        url: URL fetched by GitHub API
    """
    
    # Celery task to work in the background
    save_requirements_task.delay(repo_name)
        