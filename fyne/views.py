from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from checkpoints.models import DailyCheckpoint, UVReading
from products.models import ProductUsage
from progress.models import ProgressRecord
from datetime import date

@login_required
def dashboard(request):
    """Main dashboard view"""
    # Get today's checkpoint
    today_checkpoint = DailyCheckpoint.objects.filter(
        user=request.user,
        timestamp__date=date.today()
    ).first()
    
    # Get latest progress
    latest_progress = ProgressRecord.objects.filter(user=request.user).first()
    
    # Get active products
    active_products = ProductUsage.objects.filter(
        user=request.user,
        end_date__isnull=True
    )[:5]
    
    # Get recent checkpoints for quick stats
    recent_checkpoints = DailyCheckpoint.objects.filter(user=request.user)[:7]
    
    # Get latest UV reading
    latest_uv = UVReading.objects.filter(user=request.user).first()
    
    context = {
        'today_checkpoint': today_checkpoint,
        'latest_progress': latest_progress,
        'active_products': active_products,
        'recent_checkpoints': recent_checkpoints,
        'latest_uv': latest_uv,
    }
    
    return render(request, 'dashboard.html', context)
