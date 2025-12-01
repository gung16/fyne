from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile with skincare-specific information"""
    SKIN_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('oily', 'Oily'),
        ('dry', 'Dry'),
        ('combination', 'Combination'),
        ('sensitive', 'Sensitive'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES, default='normal')
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        db_table = 'user_profile'
