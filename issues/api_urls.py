from django.urls import path
from . import api_views

urlpatterns = [
    path('issues/', api_views.issue_list_api, name='api_issue_list'),
    path('issues/<uuid:issue_id>/', api_views.issue_detail_api, name='api_issue_detail'),
    path('stats/', api_views.stats_api, name='api_stats'),
]
