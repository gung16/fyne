from django.urls import path
from . import views

app_name = 'checkpoints'

urlpatterns = [
    path('daily/', views.daily_checkpoint, name='daily_checkpoint'),
    path('detail/<int:pk>/', views.checkpoint_detail, name='checkpoint_detail'),
    path('history/', views.checkpoint_history, name='checkpoint_history'),
    path('uv/', views.uv_tracker, name='uv_tracker'),
]
