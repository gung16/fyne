from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.progress_view, name='progress_view'),
    path('insights/', views.insights, name='insights'),
]
