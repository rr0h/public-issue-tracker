from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Issue(models.Model):
    """Main Issue model for tracking community problems"""
    
    CATEGORY_CHOICES = [
        ('pothole', 'Pothole'),
        ('garbage', 'Garbage/Waste'),
        ('street_light', 'Broken Street Light'),
        ('water_leak', 'Water Leakage'),
        ('drainage', 'Drainage Problem'),
        ('road_damage', 'Road Damage'),
        ('electricity', 'Electricity Issue'),
        ('other', 'Other'),
    ]
    
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    # Unique identifier
    issue_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Basic information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.TextField()
    
    # Photos
    photo_before = models.ImageField(upload_to='issues/before/')
    
    # Status and priority
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Assignment
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_issues'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.issue_id} - {self.title}"
    
    @property
    def resolution_time(self):
        """Calculate resolution time in days"""
        if self.resolved_at:
            delta = self.resolved_at - self.created_at
            return delta.days
        return None
    
    @property
    def is_resolved(self):
        return self.status == 'resolved'
    
    def save(self, *args, **kwargs):
        # Set resolved_at when status changes to resolved
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)


class IssuePhoto(models.Model):
    """Additional photos for an issue"""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='additional_photos')
    photo = models.ImageField(upload_to='issues/additional/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.issue.issue_id}"


class IssueUpdate(models.Model):
    """Track status updates and comments on issues"""
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='updates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Issue.STATUS_CHOICES)
    comment = models.TextField()
    photo_after = models.ImageField(upload_to='issues/after/', null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='update_assignments'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Update for {self.issue.issue_id} - {self.status}"


class Comment(models.Model):
    """Comments on issues"""
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    is_toxic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.issue.issue_id}"
