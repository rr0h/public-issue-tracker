from django.contrib import admin
from .models import Issue, IssueUpdate, Comment, IssuePhoto


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """Issue admin configuration"""
    list_display = ['issue_id', 'title', 'category', 'status', 'urgency_level', 'user', 'created_at']
    list_filter = ['status', 'category', 'urgency_level', 'created_at']
    search_fields = ['title', 'description', 'issue_id', 'user__username']
    readonly_fields = ['issue_id', 'created_at', 'updated_at', 'resolved_at']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('issue_id', 'user', 'title', 'category', 'description')
        }),
        ('Location', {
            'fields': ('address', 'latitude', 'longitude')
        }),
        ('Status & Priority', {
            'fields': ('status', 'urgency_level', 'assigned_to')
        }),
        ('Media', {
            'fields': ('photo_before',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at')
        }),
    )


@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    """Issue update admin configuration"""
    list_display = ['issue', 'status', 'user', 'assigned_to', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['issue__title', 'comment']
    readonly_fields = ['timestamp']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin configuration"""
    list_display = ['issue', 'user', 'text_preview', 'is_toxic', 'created_at']
    list_filter = ['is_toxic', 'created_at']
    search_fields = ['text', 'user__username', 'issue__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'


@admin.register(IssuePhoto)
class IssuePhotoAdmin(admin.ModelAdmin):
    """Issue photo admin configuration"""
    list_display = ['issue', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['issue__title']
    readonly_fields = ['uploaded_at']
