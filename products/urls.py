from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('add-to-routine/<int:pk>/', views.add_to_routine, name='add_to_routine'),
    path('ingredient-safety/', views.ingredient_safety, name='ingredient_safety'),
    path('check-safety/<int:pk>/', views.check_product_safety, name='check_product_safety'),
]
