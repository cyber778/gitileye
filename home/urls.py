from django.urls import path

from . import views

urlpatterns = [
    # path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
    path('', views.HomeView.as_view(), name="home")
]