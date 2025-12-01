from django.db import models
from django.contrib.auth.models import User

class DailyCheckpoint(models.Model):
    """Daily skin checkpoint from front camera scan"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkpoints')
    
    # Skin metrics (scores from 0-100)
    acne_level = models.IntegerField(default=0, help_text="Acne severity score (0-100)")
    oil_level = models.IntegerField(default=0, help_text="Oil/sebum level (0-100)")
    dark_spot_score = models.IntegerField(default=0, help_text="Dark spots/hyperpigmentation (0-100)")
    redness_score = models.IntegerField(default=0, help_text="Redness/inflammation (0-100)")
    hydration_score = models.IntegerField(default=0, help_text="Skin hydration level (0-100)")
    texture_score = models.IntegerField(default=0, help_text="Skin texture quality (0-100)")
    
    # Optional: store image of the scan
    scan_image = models.ImageField(upload_to='checkpoints/', null=True, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def overall_score(self):
        """Calculate overall skin health score"""
        scores = [
            100 - self.acne_level,
            100 - self.oil_level,
            100 - self.dark_spot_score,
            100 - self.redness_score,
            self.hydration_score,
            self.texture_score
        ]
        return sum(scores) / len(scores)
    
    class Meta:
        db_table = 'daily_checkpoint'
        ordering = ['-timestamp']


class UVReading(models.Model):
    """Daily UV and environmental exposure data"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uv_readings')
    
    uv_index = models.DecimalField(max_digits=4, decimal_places=2, help_text="UV Index value")
    humidity = models.DecimalField(max_digits=5, decimal_places=2, help_text="Humidity percentage")
    pollution_level = models.IntegerField(default=0, help_text="Air quality index (0-500)")
    
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - UV {self.uv_index} - {self.timestamp.strftime('%Y-%m-%d')}"
    
    class Meta:
        db_table = 'uv_reading'
        ordering = ['-timestamp']
