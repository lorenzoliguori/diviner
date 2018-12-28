from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'invest_home/', views.invest_home, name='invest_home'),    
    path(r'invest_request/', views.invest_request, name='invest_request'),
    path(r'retire_home/', views.retire_home, name='retire_home'),    
    path(r'retire_request/', views.retire_request, name='retire_request'),
    path(r'commit_home/', views.commit_home, name='commit_home'),    
    path(r'commit_request/', views.commit_request, name='commit_request'),        
]
