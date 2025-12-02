from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DailyCheckpoint, UVReading
from progress.models import ProgressRecord
import requests
from datetime import date

@login_required
def daily_checkpoint(request):
    """Create daily skin checkpoint with AI camera analysis (using random values for prototype)"""
    if request.method == 'POST':
        # Simulate AI computer vision analysis with random values
        import random
        
        checkpoint = DailyCheckpoint.objects.create(
            user=request.user,
            acne_level=random.randint(15, 45),
            oil_level=random.randint(20, 60),
            dark_spot_score=random.randint(10, 40),
            redness_score=random.randint(5, 35),
            hydration_score=random.randint(50, 85),
            texture_score=random.randint(55, 90),
            notes='Auto-analyzed via camera scan',
        )
        
        # Create progress record
        progress = ProgressRecord.objects.create(
            user=request.user,
            checkpoint=checkpoint,
            overall_skin_score=checkpoint.overall_score
        )
        progress.calculate_score()
        progress.analyze_trend()
        
        messages.success(request, 'Skin analysis completed successfully!')
        return redirect('checkpoints:checkpoint_detail', pk=checkpoint.pk)
    
    return render(request, 'checkpoints/daily_checkpoint.html')

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
