from django.http import JsonResponse
from django.db.models import Count
from .models import Issue


def issue_list_api(request):
    """API endpoint for issue list"""
    issues = Issue.objects.all()
    
    # Apply filters
    category = request.GET.get('category')
    status = request.GET.get('status')
    
    if category:
        issues = issues.filter(category=category)
    if status:
        issues = issues.filter(status=status)
    
    data = []
    for issue in issues:
        data.append({
            'id': str(issue.issue_id),
            'title': issue.title,
            'category': issue.category,
            'status': issue.status,
            'urgency_level': issue.urgency_level,
            'address': issue.address,
            'latitude': float(issue.latitude) if issue.latitude else None,
            'longitude': float(issue.longitude) if issue.longitude else None,
            'created_at': issue.created_at.isoformat(),
            'user': issue.user.username,
        })
    
    return JsonResponse({'issues': data})


def issue_detail_api(request, issue_id):
    """API endpoint for issue detail"""
    try:
        issue = Issue.objects.get(issue_id=issue_id)
        data = {
            'id': str(issue.issue_id),
            'title': issue.title,
            'category': issue.category,
            'description': issue.description,
            'status': issue.status,
            'urgency_level': issue.urgency_level,
            'address': issue.address,
            'latitude': float(issue.latitude) if issue.latitude else None,
            'longitude': float(issue.longitude) if issue.longitude else None,
            'created_at': issue.created_at.isoformat(),
            'updated_at': issue.updated_at.isoformat(),
            'user': issue.user.username,
            'assigned_to': issue.assigned_to.username if issue.assigned_to else None,
        }
        return JsonResponse(data)
    except Issue.DoesNotExist:
        return JsonResponse({'error': 'Issue not found'}, status=404)


def stats_api(request):
    """API endpoint for statistics"""
    total_issues = Issue.objects.count()
    issues_by_status = Issue.objects.values('status').annotate(count=Count('id'))
    issues_by_category = Issue.objects.values('category').annotate(count=Count('id'))
    
    data = {
        'total_issues': total_issues,
        'by_status': list(issues_by_status),
        'by_category': list(issues_by_category),
    }
    
    return JsonResponse(data)
