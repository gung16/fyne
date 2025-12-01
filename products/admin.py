from django.contrib import admin
from .models import SkincareProduct, ProductUsage, IngredientSafety

@admin.register(SkincareProduct)
class SkincareProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'created_at')
    list_filter = ('category', 'brand', 'created_at')
    search_fields = ('name', 'brand', 'description')

@admin.register(ProductUsage)
class ProductUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'frequency', 'start_date', 'is_active')
    list_filter = ('frequency', 'start_date', 'end_date')
    search_fields = ('user__username', 'product__name')
    
    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = 'Active'

@admin.register(IngredientSafety)
class IngredientSafetyAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'risk_level', 'checked_at')
    list_filter = ('risk_level', 'checked_at')
    search_fields = ('user__username', 'product__name', 'notes')
