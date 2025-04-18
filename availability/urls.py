from django.urls import path
from . import views

urlpatterns = [
    path('solo-grid/', views.solo_availability_grid, name='solo_availability_grid'),
    path('group-grid/', views.group_availability_grid, name='group_availability_grid'),
    
]
