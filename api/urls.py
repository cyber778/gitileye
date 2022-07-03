from django.urls import path
from . import views

urlpatterns = [
    path('top-repos/<int:top_n>/', views.fetch_top_repos),
    path('name/<path:repo_name>/', views.fetch_specific_repo),
    path('status/<path:repo_name>/', views.get_status, name='get_status'),
]
