"""
AI utilities for issue tracking
Includes duplicate detection and toxicity filtering
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class DuplicateDetector:
    """Detect duplicate issues using TF-IDF and cosine similarity"""
    
    @staticmethod
    def find_similar_issues(new_issue_text, existing_issues, threshold=0.6):
        """
        Find similar issues based on text similarity
        
        Args:
            new_issue_text: Text of the new issue (title + description)
            existing_issues: List of existing issues with text
            threshold: Similarity threshold (0-1)
        
        Returns:
            List of similar issues
        """
        if not existing_issues:
            return []
        
        # Prepare texts
        texts = [new_issue_text] + [issue['text'] for issue in existing_issues]
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            
            # Find similar issues
            similar_issues = []
            for idx, similarity in enumerate(similarities):
                if similarity >= threshold:
                    similar_issues.append({
                        'issue': existing_issues[idx],
                        'similarity': float(similarity)
                    })
            
            # Sort by similarity
            similar_issues.sort(key=lambda x: x['similarity'], reverse=True)
            return similar_issues
        except:
            return []
    
    @staticmethod
    def check_location_proximity(lat1, lon1, lat2, lon2, max_distance_km=1.0):
        """
        Check if two locations are within proximity
        Uses Haversine formula
        
        Args:
            lat1, lon1: First location coordinates
            lat2, lon2: Second location coordinates
            max_distance_km: Maximum distance in kilometers
        
        Returns:
            Boolean indicating if locations are close
        """
        from math import radians, sin, cos, sqrt, atan2
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = 6371 * c  # Earth radius in km
        
        return distance <= max_distance_km


class ToxicityFilter:
    """Simple toxicity filter for comments"""
    
    # List of toxic words/patterns
    TOXIC_WORDS = [
        'stupid', 'idiot', 'dumb', 'hate', 'kill', 'die', 'worst',
        'useless', 'garbage', 'trash', 'pathetic', 'loser', 'fool',
        'damn', 'hell', 'crap', 'suck', 'terrible', 'horrible'
    ]
    
    @staticmethod
    def is_toxic(text, threshold=2):
        """
        Check if text contains toxic content
        
        Args:
            text: Text to check
            threshold: Number of toxic words to trigger filter
        
        Returns:
            Boolean indicating if text is toxic
        """
        text_lower = text.lower()
        toxic_count = 0
        
        for word in ToxicityFilter.TOXIC_WORDS:
            if word in text_lower:
                toxic_count += 1
        
        return toxic_count >= threshold
    
    @staticmethod
    def clean_text(text):
        """Remove or replace toxic words"""
        text_lower = text.lower()
        for word in ToxicityFilter.TOXIC_WORDS:
            if word in text_lower:
                text = re.sub(word, '***', text, flags=re.IGNORECASE)
        return text


class PriorityClassifier:
    """Classify issue priority based on keywords"""
    
    HIGH_PRIORITY_KEYWORDS = [
        'emergency', 'urgent', 'dangerous', 'hazard', 'accident', 'injury',
        'severe', 'critical', 'immediate', 'life-threatening', 'major'
    ]
    
    LOW_PRIORITY_KEYWORDS = [
        'minor', 'small', 'cosmetic', 'aesthetic', 'non-urgent', 'eventually'
    ]
    
    @staticmethod
    def suggest_priority(title, description):
        """
        Suggest priority level based on text analysis
        
        Args:
            title: Issue title
            description: Issue description
        
        Returns:
            Suggested priority ('high', 'medium', 'low')
        """
        text = (title + ' ' + description).lower()
        
        # Check for high priority keywords
        high_count = sum(1 for keyword in PriorityClassifier.HIGH_PRIORITY_KEYWORDS if keyword in text)
        low_count = sum(1 for keyword in PriorityClassifier.LOW_PRIORITY_KEYWORDS if keyword in text)
        
        if high_count >= 2:
            return 'high'
        elif low_count >= 2:
            return 'low'
        elif high_count > low_count:
            return 'high'
        elif low_count > high_count:
            return 'low'
        else:
            return 'medium'
