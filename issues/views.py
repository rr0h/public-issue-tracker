from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Issue, IssueUpdate, Comment, IssuePhoto
from .forms import IssueCreateForm, IssueUpdateForm, CommentForm, IssueFilterForm
from .ai_utils import DuplicateDetector, ToxicityFilter, PriorityClassifier
from accounts.models import User


def home_view(request):
    """Home page with overview"""
    recent_issues = Issue.objects.all()[:6]
    resolved_count = Issue.objects.filter(status='resolved').count()
    pending_count = Issue.objects.filter(status='pending').count()
    total_count = Issue.objects.count()
    
    context = {
        'recent_issues': recent_issues,
        'resolved_count': resolved_count,
        'pending_count': pending_count,
        'total_count': total_count,
    }
    return render(request, 'issues/home.html', context)


def issue_list_view(request):
    """List all issues with filters"""
    issues = Issue.objects.all()
    
    # Apply filters
    filter_form = IssueFilterForm(request.GET)
    if filter_form.is_valid():
        category = filter_form.cleaned_data.get('category')
        status = filter_form.cleaned_data.get('status')
        urgency = filter_form.cleaned_data.get('urgency')
        sort_by = filter_form.cleaned_data.get('sort_by') or '-created_at'
        
        if category:
            issues = issues.filter(category=category)
        if status:
            issues = issues.filter(status=status)
        if urgency:
            issues = issues.filter(urgency_level=urgency)
        
        issues = issues.order_by(sort_by)
    
    context = {
        'issues': issues,
        'filter_form': filter_form,
    }
    return render(request, 'issues/issue_list.html', context)


@login_required
def issue_create_view(request):
    """Create new issue"""
    if request.method == 'POST':
        form = IssueCreateForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            
            # AI: Suggest priority
            suggested_priority = PriorityClassifier.suggest_priority(
                issue.title, issue.description
            )
            if suggested_priority != issue.urgency_level:
                messages.info(
                    request, 
                    f'AI suggests priority: {suggested_priority.upper()}. You selected: {issue.urgency_level.upper()}'
                )
            
            issue.save()
            
            # Handle additional photos
            additional_photos = request.FILES.getlist('additional_photos')
            for photo in additional_photos:
                IssuePhoto.objects.create(issue=issue, photo=photo)
            
            # AI: Check for duplicates
            similar_text = f"{issue.title} {issue.description}"
            existing_issues = Issue.objects.filter(
                category=issue.category,
                status__in=['pending', 'reviewed', 'assigned', 'in_progress']
            ).exclude(id=issue.id)
            
            existing_data = [
                {
                    'text': f"{i.title} {i.description}",
                    'id': i.id,
                    'issue_id': str(i.issue_id),
                    'lat': i.latitude,
                    'lon': i.longitude
                }
                for i in existing_issues
            ]
            
            similar_issues = DuplicateDetector.find_similar_issues(similar_text, existing_data)
            
            # Check location proximity for similar issues
            nearby_duplicates = []
            if issue.latitude and issue.longitude:
                for similar in similar_issues:
                    similar_issue = similar['issue']
                    if similar_issue['lat'] and similar_issue['lon']:
                        if DuplicateDetector.check_location_proximity(
                            issue.latitude, issue.longitude,
                            similar_issue['lat'], similar_issue['lon']
                        ):
                            nearby_duplicates.append(similar)
            
            if nearby_duplicates:
                messages.warning(
                    request,
                    f'Similar issue(s) found nearby! Check issue #{nearby_duplicates[0]["issue"]["issue_id"]}'
                )
            
            messages.success(request, f'Issue created successfully! Issue ID: {issue.issue_id}')
            return redirect('issue_detail', issue_id=issue.issue_id)
    else:
        form = IssueCreateForm()
    
    return render(request, 'issues/issue_create.html', {'form': form})


def issue_detail_view(request, issue_id):
    """View issue details"""
    issue = get_object_or_404(Issue, issue_id=issue_id)
    updates = issue.updates.all()
    comments = issue.comments.filter(is_toxic=False)
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.issue = issue
            comment.user = request.user
            
            # AI: Check toxicity
            if ToxicityFilter.is_toxic(comment.text):
                comment.is_toxic = True
                messages.error(request, 'Your comment contains inappropriate content and has been flagged.')
            else:
                messages.success(request, 'Comment added successfully!')
            
            comment.save()
            return redirect('issue_detail', issue_id=issue_id)
    else:
        comment_form = CommentForm()
    
    context = {
        'issue': issue,
        'updates': updates,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'issues/issue_detail.html', context)


@login_required
def my_issues_view(request):
    """View user's own issues"""
    issues = Issue.objects.filter(user=request.user)
    
    context = {
        'issues': issues,
    }
    return render(request, 'issues/my_issues.html', context)


def resolved_gallery_view(request):
    """Public gallery of resolved issues"""
    resolved_issues = Issue.objects.filter(status='resolved').order_by('-resolved_at')
    
    # Get issues with after photos
    issues_with_photos = []
    for issue in resolved_issues:
        after_update = issue.updates.filter(photo_after__isnull=False).first()
        if after_update:
            issues_with_photos.append({
                'issue': issue,
                'after_photo': after_update.photo_after
            })
    
    context = {
        'issues_with_photos': issues_with_photos,
    }
    return render(request, 'issues/resolved_gallery.html', context)


def map_view(request):
    """Interactive map view of all issues"""
    issues = Issue.objects.filter(latitude__isnull=False, longitude__isnull=False)
    
    # Prepare data for map
    issues_data = []
    for issue in issues:
        issues_data.append({
            'id': str(issue.issue_id),
            'title': issue.title,
            'category': issue.get_category_display(),
            'status': issue.status,
            'urgency': issue.urgency_level,
            'lat': float(issue.latitude),
            'lng': float(issue.longitude),
            'address': issue.address,
        })
    
    context = {
        'issues_data': issues_data,
    }
    return render(request, 'issues/map.html', context)


# Admin Views
@login_required
def admin_dashboard_view(request):
    """Admin dashboard with analytics"""
    if not request.user.is_admin and not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    # Statistics
    total_issues = Issue.objects.count()
    pending_issues = Issue.objects.filter(status='pending').count()
    in_progress_issues = Issue.objects.filter(status='in_progress').count()
    resolved_issues = Issue.objects.filter(status='resolved').count()
    
    # Issues by category
    issues_by_category = Issue.objects.values('category').annotate(count=Count('id'))
    
    # Issues by status
    issues_by_status = Issue.objects.values('status').annotate(count=Count('id'))
    
    # Recent issues
    recent_issues = Issue.objects.all()[:10]
    
    # Average resolution time
    resolved = Issue.objects.filter(status='resolved', resolved_at__isnull=False)
    avg_resolution_days = 0
    if resolved.exists():
        total_days = sum([issue.resolution_time or 0 for issue in resolved])
        avg_resolution_days = total_days / resolved.count()
    
    context = {
        'total_issues': total_issues,
        'pending_issues': pending_issues,
        'in_progress_issues': in_progress_issues,
        'resolved_issues': resolved_issues,
        'issues_by_category': list(issues_by_category),
        'issues_by_status': list(issues_by_status),
        'recent_issues': recent_issues,
        'avg_resolution_days': round(avg_resolution_days, 1),
    }
    return render(request, 'issues/admin_dashboard.html', context)


@login_required
def admin_issue_manage_view(request, issue_id):
    """Admin: Manage specific issue"""
    if not request.user.is_admin and not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    issue = get_object_or_404(Issue, issue_id=issue_id)
    
    if request.method == 'POST':
        form = IssueUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.issue = issue
            update.user = request.user
            update.save()
            
            # Update issue status and assignment
            issue.status = update.status
            if update.assigned_to:
                issue.assigned_to = update.assigned_to
            issue.save()
            
            messages.success(request, 'Issue updated successfully!')
            return redirect('issue_detail', issue_id=issue_id)
    else:
        form = IssueUpdateForm(initial={'status': issue.status})
    
    # Get workers for assignment
    workers = User.objects.filter(Q(role='worker') | Q(role='admin'))
    form.fields['assigned_to'].queryset = workers
    
    context = {
        'issue': issue,
        'form': form,
    }
    return render(request, 'issues/admin_manage_issue.html', context)
