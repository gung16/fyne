from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DailyCheckpoint, UVReading
from progress.models import ProgressRecord
import requests
from datetime import date

@login_required
def daily_checkpoint(request):
    """Create daily skin checkpoint"""
    if request.method == 'POST':
        checkpoint = DailyCheckpoint.objects.create(
            user=request.user,
            acne_level=int(request.POST.get('acne_level', 0)),
            oil_level=int(request.POST.get('oil_level', 0)),
            dark_spot_score=int(request.POST.get('dark_spot_score', 0)),
            redness_score=int(request.POST.get('redness_score', 0)),
            hydration_score=int(request.POST.get('hydration_score', 0)),
            texture_score=int(request.POST.get('texture_score', 0)),
            notes=request.POST.get('notes', ''),
        )
        
        # Create progress record
        progress = ProgressRecord.objects.create(
            user=request.user,
            checkpoint=checkpoint,
            overall_skin_score=checkpoint.overall_score
        )
        progress.calculate_score()
        progress.analyze_trend()
        
        messages.success(request, 'Daily checkpoint recorded successfully!')
        return redirect('checkpoints:checkpoint_detail', pk=checkpoint.pk)
    
    # Check if already done today
    today_checkpoint = DailyCheckpoint.objects.filter(
        user=request.user,
        timestamp__date=date.today()
    ).first()
    
    return render(request, 'checkpoints/daily_checkpoint.html', {
        'today_checkpoint': today_checkpoint
    })

@login_required
def checkpoint_detail(request, pk):
    """View checkpoint details"""
    checkpoint = get_object_or_404(DailyCheckpoint, pk=pk, user=request.user)
    return render(request, 'checkpoints/checkpoint_detail.html', {'checkpoint': checkpoint})

@login_required
def checkpoint_history(request):
    """View checkpoint history"""
    checkpoints = DailyCheckpoint.objects.filter(user=request.user)
    return render(request, 'checkpoints/checkpoint_history.html', {'checkpoints': checkpoints})

@login_required
def uv_tracker(request):
    """UV exposure tracker"""
    if request.method == 'POST':
        UVReading.objects.create(
            user=request.user,
            uv_index=request.POST.get('uv_index', 0),
            humidity=request.POST.get('humidity', 0),
            pollution_level=request.POST.get('pollution_level', 0),
            location=request.POST.get('location', ''),
        )
        messages.success(request, 'UV reading recorded!')
        return redirect('checkpoints:uv_tracker')
    
    readings = UVReading.objects.filter(user=request.user)[:10]
    return render(request, 'checkpoints/uv_tracker.html', {'readings': readings})
