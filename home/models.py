from django.db import models, DatabaseError
from django.db.models import UniqueConstraint
from django.shortcuts import resolve_url

from .utils import create_requiremets_for_repo

UNIQUE_ERROR_MSG = "You already have a entry with that name and version"


class RepoItem(models.Model):
    class RepoStatus(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'
        ERROR = 'error', 'Error'
        CREATED = 'created', 'Repo created, waiting for requirement gathering'

    status = models.CharField(
        max_length=20,
        choices=RepoStatus.choices,
        default=RepoStatus.CREATED,
    )
    name = models.CharField(max_length=500, unique=True)
    url = models.URLField() 
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def was_updated(self):
        return self.status in {self.RepoStatus.DONE, self.RepoStatus.IN_PROGRESS}
    
    @property
    def status_url(self):
        return resolve_url('get_status', repo_name=self.name)
    
    def save_requirements(self, force_update=False):
        """
        Create DB enteries for all requirements
        
        Args:
            update (bool, optional): if False and requirements 
            have already been saved once no action will happen.
        """
        
        if not self.was_updated or force_update:
            self.status = self.RepoStatus.IN_PROGRESS
            self.save()
            
            create_requiremets_for_repo(self.name)
            
    def __str__(self):
        return f'{self.name}'
            
    

class RepoRequirement(models.Model):
    version = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    repos = models.ManyToManyField(RepoItem, related_name='repo_requirements')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['version', 'name'], name='unique_requirement')
        ]
    
    def __str__(self):
        return f'{self.name}=={self.version}'
    