from django.db import models
from django.contrib.auth.models import User

class SkincareProduct(models.Model):
    """Skincare product catalog"""
    CATEGORY_CHOICES = [
        ('cleanser', 'Cleanser'),
        ('toner', 'Toner'),
        ('serum', 'Serum'),
        ('moisturizer', 'Moisturizer'),
        ('sunscreen', 'Sunscreen'),
        ('exfoliant', 'Exfoliant'),
        ('mask', 'Mask'),
        ('eye_cream', 'Eye Cream'),
        ('spot_treatment', 'Spot Treatment'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    ingredients = models.JSONField(default=list, help_text="List of ingredients")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.brand} - {self.name}"
    
    class Meta:
        db_table = 'skincare_product'
        ordering = ['brand', 'name']


class ProductUsage(models.Model):
    """Track when and how a product is used"""
    FREQUENCY_CHOICES = [
        ('am', 'Morning (AM)'),
        ('pm', 'Evening (PM)'),
        ('am_pm', 'Both AM & PM'),
        ('weekly', 'Weekly'),
        ('as_needed', 'As Needed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_usages')
    product = models.ForeignKey(SkincareProduct, on_delete=models.CASCADE, related_name='usages')
    
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='pm')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave empty if still using")
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.frequency})"
    
    @property
    def is_active(self):
        """Check if product is currently in use"""
        return self.end_date is None
    
    class Meta:
        db_table = 'product_usage'
        ordering = ['-start_date']


class IngredientSafety(models.Model):
    """Ingredient safety and compatibility checker"""
    RISK_LEVEL_CHOICES = [
        ('safe', 'Safe'),
        ('caution', 'Use with Caution'),
        ('avoid', 'Avoid'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingredient_checks')
    product = models.ForeignKey(SkincareProduct, on_delete=models.CASCADE, related_name='safety_checks')
    
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default='safe')
    flagged_ingredients = models.JSONField(default=list, help_text="List of problematic ingredients")
    notes = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.risk_level})"
    
    class Meta:
        db_table = 'ingredient_safety'
        ordering = ['-checked_at']
