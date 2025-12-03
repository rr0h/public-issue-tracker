from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from .models import Issue, IssueUpdate, Comment
from .ai_utils import DuplicateDetector, ToxicityFilter, PriorityClassifier


class IssueModelTest(TestCase):
    """Test Issue model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.issue = Issue.objects.create(
            user=self.user,
            title='Test Pothole',
            category='pothole',
            description='Large pothole on main street',
            address='123 Main St',
            latitude=40.7128,
            longitude=-74.0060,
            urgency_level='high'
        )
    
    def test_issue_creation(self):
        """Test issue is created correctly"""
        self.assertEqual(self.issue.title, 'Test Pothole')
        self.assertEqual(self.issue.status, 'pending')
        self.assertIsNotNone(self.issue.issue_id)
    
    def test_issue_str(self):
        """Test issue string representation"""
        self.assertIn('Test Pothole', str(self.issue))


class IssueViewTest(TestCase):
    """Test Issue views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_home_view(self):
        """Test home page loads"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Issue Tracker')
    
    def test_issue_list_view(self):
        """Test issue list page loads"""
        response = self.client.get(reverse('issue_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_issue_create_requires_login(self):
        """Test issue creation requires authentication"""
        response = self.client.get(reverse('issue_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class AIUtilsTest(TestCase):
    """Test AI utilities"""
    
    def test_toxicity_filter(self):
        """Test toxicity detection"""
        toxic_text = "This is stupid and terrible"
        clean_text = "This is a nice comment"
        
        self.assertTrue(ToxicityFilter.is_toxic(toxic_text))
        self.assertFalse(ToxicityFilter.is_toxic(clean_text))
    
    def test_priority_classifier(self):
        """Test priority classification"""
        high_priority = PriorityClassifier.suggest_priority(
            "Emergency", "Dangerous hazard, immediate attention needed"
        )
        low_priority = PriorityClassifier.suggest_priority(
            "Minor issue", "Small cosmetic problem"
        )
        
        self.assertEqual(high_priority, 'high')
        self.assertEqual(low_priority, 'low')
    
    def test_duplicate_detector(self):
        """Test duplicate detection"""
        new_text = "Large pothole on main street"
        existing = [
            {'text': 'Big pothole on main road', 'id': 1, 'issue_id': 'test-1', 'lat': 40.7128, 'lon': -74.0060}
        ]
        
        similar = DuplicateDetector.find_similar_issues(new_text, existing, threshold=0.3)
        self.assertGreater(len(similar), 0)


class CommentTest(TestCase):
    """Test Comment functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.issue = Issue.objects.create(
            user=self.user,
            title='Test Issue',
            category='pothole',
            description='Test description',
            address='Test address',
            urgency_level='medium'
        )
    
    def test_comment_creation(self):
        """Test comment is created"""
        comment = Comment.objects.create(
            issue=self.issue,
            user=self.user,
            text='This is a test comment'
        )
        
        self.assertEqual(comment.text, 'This is a test comment')
        self.assertFalse(comment.is_toxic)


class StatusWorkflowTest(TestCase):
    """Test issue status workflow"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        
        self.issue = Issue.objects.create(
            user=self.user,
            title='Test Issue',
            category='pothole',
            description='Test description',
            address='Test address',
            urgency_level='medium'
        )
    
    def test_status_update(self):
        """Test status can be updated"""
        update = IssueUpdate.objects.create(
            issue=self.issue,
            user=self.admin,
            status='reviewed',
            comment='Issue has been reviewed'
        )
        
        self.issue.status = 'reviewed'
        self.issue.save()
        
        self.assertEqual(self.issue.status, 'reviewed')
        self.assertEqual(update.status, 'reviewed')
