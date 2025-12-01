from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProgressRecord
from checkpoints.models import DailyCheckpoint
from django.db.models import Avg
from datetime import timedelta, date

@login_required
def progress_view(request):
    """View progress tracking and analytics"""
    progress_records = ProgressRecord.objects.filter(user=request.user)[:30]
    
    # Calculate statistics
    if progress_records.exists():
        avg_score = progress_records.aggregate(Avg('overall_skin_score'))['overall_skin_score__avg']
        latest = progress_records.first()
        
        # Get trend data for chart
        chart_data = []
        for record in reversed(list(progress_records)):
            chart_data.append({
                'date': record.timestamp.strftime('%m/%d'),
                'score': float(record.overall_skin_score)
            })
    else:
        avg_score = 0
        latest = None
        chart_data = []
    
    context = {
        'progress_records': progress_records,
        'avg_score': avg_score,
        'latest': latest,
        'chart_data': chart_data,
    }
    return render(request, 'progress/progress_view.html', context)

@login_required
def insights(request):
    """AI-generated insights and recommendations"""
    progress_records = ProgressRecord.objects.filter(user=request.user)[:7]
    
    insights_list = []
    
    if progress_records.count() >= 3:
        improving_count = sum(1 for p in progress_records if p.improvement_trend == 'improving')
        declining_count = sum(1 for p in progress_records if p.improvement_trend == 'declining')
        
        if improving_count > declining_count:
            insights_list.append({
                'type': 'success',
                'title': 'Great Progress!',
                'message': 'Your skin is showing improvement. Keep up your current routine!'
            })
        elif declining_count > improving_count:
            insights_list.append({
                'type': 'warning',
                'title': 'Needs Attention',
                'message': 'Your skin metrics are declining. Consider reviewing your products or consulting a dermatologist.'
            })
    
    return render(request, 'progress/insights.html', {'insights': insights_list})
