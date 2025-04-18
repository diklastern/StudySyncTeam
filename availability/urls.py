from django.urls import path
from . import views

urlpatterns = [
    path('solo/', views.solo_availability_view, name='solo_availability'),
    path('group/', views.group_availability_view, name='group_availability'),
    path('solo-grid/', views.solo_availability_grid, name='solo_availability_grid'),
    
]
