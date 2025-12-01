from django.contrib import admin
from .models import ProgressRecord

@admin.register(ProgressRecord)
class ProgressRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'overall_skin_score', 'improvement_trend', 'timestamp')
    list_filter = ('improvement_trend', 'timestamp', 'user')
    search_fields = ('user__username', 'insight_notes')
    readonly_fields = ('timestamp',)
