from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from checkpoints.models import DailyCheckpoint
from products.models import ProductUsage
from progress.models import ProgressRecord

@login_required
def profile_view(request):
    """User profile page"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get user statistics
    total_checkpoints = DailyCheckpoint.objects.filter(user=request.user).count()
    active_products = ProductUsage.objects.filter(user=request.user, end_date__isnull=True).count()
    latest_progress = ProgressRecord.objects.filter(user=request.user).first()
    
    context = {
        'profile': profile,
        'total_checkpoints': total_checkpoints,
        'active_products': active_products,
        'latest_progress': latest_progress,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
    """Edit user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.skin_type = request.POST.get('skin_type', profile.skin_type)
        profile.age = request.POST.get('age') or None
        profile.location = request.POST.get('location', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    
    return render(request, 'users/profile_edit.html', {'profile': profile})
