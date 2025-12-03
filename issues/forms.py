from django import forms
from .models import Issue, IssueUpdate, Comment, IssuePhoto


class IssueCreateForm(forms.ModelForm):
    """Form for creating new issues"""
    
    additional_photos = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        help_text='Upload additional photos (optional)'
    )
    
    class Meta:
        model = Issue
        fields = ['title', 'category', 'description', 'address', 'latitude', 'longitude', 
                  'photo_before', 'urgency_level']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['latitude', 'longitude']:
                self.fields[field].widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                })


class IssueUpdateForm(forms.ModelForm):
    """Form for updating issue status (Admin only)"""
    
    class Meta:
        model = IssueUpdate
        fields = ['status', 'comment', 'photo_after', 'assigned_to']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })


class CommentForm(forms.ModelForm):
    """Form for adding comments"""
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add your comment...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })


class IssueFilterForm(forms.Form):
    """Form for filtering issues"""
    
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + Issue.CATEGORY_CHOICES,
        required=False
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Issue.STATUS_CHOICES,
        required=False
    )
    urgency = forms.ChoiceField(
        choices=[('', 'All Urgency')] + Issue.URGENCY_CHOICES,
        required=False
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('-created_at', 'Most Recent'),
            ('created_at', 'Oldest First'),
            ('-urgency_level', 'High Priority'),
        ],
        required=False,
        initial='-created_at'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })
