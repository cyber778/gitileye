from turtle import update
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from home.git_api import GithubClientException
from home.models import RepoItem
from home.utils import get_top_repos, get_url_from_repo


@api_view(['GET'])
def fetch_top_repos(request, top_n):
    status_urls = []
    try:
        repos = get_top_repos(top_n)
    except GithubClientException as e:
         return NotFound({"error": str(e)})
    for name, url in repos:
        repo, created = RepoItem.objects.get_or_create(url=url, name=name)
        status_urls.append((repo.name, repo.status_url))
        if created:
            repo.save_requirements()
    
    data = {"status_links": status_urls}
    return Response(data)


@api_view(['GET'])
def fetch_specific_repo(request, repo_name):
    try:
        url = get_url_from_repo(repo_name)
    except GithubClientException as e:
         return NotFound({"error": str(e)})
    repo, created = RepoItem.objects.get_or_create(url=url, name=repo_name)
    if created:
        repo.save_requirements()
    return Response({"status_url":repo.status_url})


@api_view(['GET'])
def get_status(request, repo_name):
    repo = RepoItem.objects.get(name=repo_name)
    data = {'status': f'{repo.status}, Last modified: {repo.modified}'}
    return Response(data)