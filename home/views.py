from django.conf import settings
from django.views.generic import TemplateView
from pkg_resources import Requirement

from home.git_api import GithubClient, GithubRepo

class HomeView(TemplateView):
    """ 
    This view is used for test purposes
    """
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        
        # from .models import RepoItem
        # repo = RepoItem.objects.get(name="vinta/awesome-python")
        # repo.save_requirements(True)
        
        return {"user":{'name': 'Elad', 'mood': 'Happy'}}
        