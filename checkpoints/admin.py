from django.contrib import admin
from .models import DailyCheckpoint, UVReading

@admin.register(DailyCheckpoint)
class DailyCheckpointAdmin(admin.ModelAdmin):
    list_display = ('user', 'overall_score', 'acne_level', 'oil_level', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'notes')
    readonly_fields = ('timestamp', 'overall_score')
    
    def overall_score(self, obj):
        return f"{obj.overall_score:.1f}"
    overall_score.short_description = 'Overall Score'

@admin.register(UVReading)
class UVReadingAdmin(admin.ModelAdmin):
    list_display = ('user', 'uv_index', 'humidity', 'pollution_level', 'location', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'location')
    readonly_fields = ('timestamp',)
