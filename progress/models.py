from django.db import models
from django.contrib.auth.models import User
from checkpoints.models import DailyCheckpoint, UVReading

class ProgressRecord(models.Model):
    """Daily progress summary combining checkpoint + UV + product usage"""
    TREND_CHOICES = [
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('declining', 'Declining'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    checkpoint = models.OneToOneField(DailyCheckpoint, on_delete=models.CASCADE, related_name='progress')
    uv_reading = models.ForeignKey(UVReading, on_delete=models.SET_NULL, null=True, blank=True, related_name='progress_records')
    
    overall_skin_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Calculated skin health score")
    improvement_trend = models.CharField(max_length=20, choices=TREND_CHOICES, default='stable')
    insight_notes = models.TextField(blank=True, help_text="AI-generated or manual insights")
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Score: {self.overall_skin_score} ({self.improvement_trend})"
    
    def calculate_score(self):
        """Calculate overall skin score from checkpoint data"""
        if self.checkpoint:
            self.overall_skin_score = self.checkpoint.overall_score
            self.save()
    
    def analyze_trend(self):
        """Compare with previous records to determine trend"""
        previous_records = ProgressRecord.objects.filter(
            user=self.user,
            timestamp__lt=self.timestamp
        ).order_by('-timestamp')[:7]  # Last 7 days
        
        if previous_records.exists():
            avg_previous = sum(r.overall_skin_score for r in previous_records) / len(previous_records)
            diff = float(self.overall_skin_score) - float(avg_previous)
            
            if diff > 5:
                self.improvement_trend = 'improving'
            elif diff < -5:
                self.improvement_trend = 'declining'
            else:
                self.improvement_trend = 'stable'
            self.save()
    
    class Meta:
        db_table = 'progress_record'
        ordering = ['-timestamp']
