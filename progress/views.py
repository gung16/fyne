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
    # Get the most recent score
    latest_record = ProgressRecord.objects.filter(user=request.user).first()
    latest_score = None
    
    if latest_record:
        latest_score = latest_record.overall_skin_score
    else:
        # Fallback to latest checkpoint if no progress record exists
        from checkpoints.models import DailyCheckpoint
        latest_checkpoint = DailyCheckpoint.objects.filter(user=request.user).first()
        if latest_checkpoint:
            latest_score = latest_checkpoint.overall_score
    
    context = {
        'latest_score': latest_score,
    }
    
    return render(request, 'progress/insights.html', context)
