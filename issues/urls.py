from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home_view, name='home'),
    path('issues/', views.issue_list_view, name='issue_list'),
    path('issues/create/', views.issue_create_view, name='issue_create'),
    path('issues/<uuid:issue_id>/', views.issue_detail_view, name='issue_detail'),
    path('my-issues/', views.my_issues_view, name='my_issues'),
    path('resolved-gallery/', views.resolved_gallery_view, name='resolved_gallery'),
    path('map/', views.map_view, name='map'),
    
    # Admin pages
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/issues/<uuid:issue_id>/manage/', views.admin_issue_manage_view, name='admin_manage_issue'),
]
