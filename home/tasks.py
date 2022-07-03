from __future__ import absolute_import, unicode_literals
from click import echo

from django.conf import settings
from django.db import DatabaseError

from .git_api import GithubRepo, GithubClientException

from celery import shared_task


@shared_task
def save_requirements_task(repo_name):
    """
    Save requirements in the bg in one bg task.
    Alternitively, each save can be a seperate celery task
    """
    # Avoid circular import for RepoRequirement
    from .models import RepoRequirement, RepoItem
    
    repo = RepoItem.objects.get(name=repo_name)
    try:
        token = getattr(settings, 'GITHUB_TOKEN', '')
        gh = GithubRepo(repo.url, token)
        
        requirements = gh.get_python_req_file_single_api()
        # remove last item since it's empty
        requirements = requirements.split('\n')[:-1] if requirements else []
        
        for requirement in requirements:
            if '==' not in requirement:
                continue
            name, version = requirement.split('==')
            req, created = RepoRequirement.objects.get_or_create(name=name, version=version)
            # Another approach here is to bulk save by creating a values_list of all the 
            # requirements and move the attribute to the RepoItem class but there will
            # be more points of failure and this way is safer
            req.repos.add(repo)
    except (DatabaseError, GithubClientException) as e:
        # DB errors or GitHub API Errors should update status of object
        repo.status = RepoItem.RepoStatus.ERROR
        repo.save()
        raise e
    repo.status = RepoItem.RepoStatus.DONE
    repo.save()
