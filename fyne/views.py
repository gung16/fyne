from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
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

def custom_login(request):
    """Custom login view that auto-accepts admin/admin123"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        try:
            # Auto-accept admin/admin123
            if username == 'admin' and password == 'admin123':
                # Check if admin user exists, create if not
                from django.contrib.auth.models import User
                try:
                    user = User.objects.get(username='admin')
                    # Ensure password is correct
                    if not user.check_password('admin123'):
                        user.set_password('admin123')
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        username='admin',
                        password='admin123',
                        email='admin@fyne.com',
                        is_staff=True,
                        is_superuser=True
                    )
                
                # Authenticate and login
                user = authenticate(request, username='admin', password='admin123')
                if user:
                    login(request, user)
                    # Force session save
                    request.session.save()
                    messages.success(request, 'Welcome back!')
                    # Use redirect with next parameter support
                    next_url = request.GET.get('next', '/')
                    from django.http import HttpResponseRedirect
                    return HttpResponseRedirect(next_url)
            
            # Try normal authentication for other users
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # Force session save
                request.session.save()
                messages.success(request, 'Welcome back!')
                next_url = request.GET.get('next', '/')
                from django.http import HttpResponseRedirect
                return HttpResponseRedirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        except Exception as e:
            messages.error(request, 'Database connection error. Please try again later.')
    
    return render(request, 'login.html')
