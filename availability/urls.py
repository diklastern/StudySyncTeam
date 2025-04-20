from django.urls import path
from .views import availability_grid_view

urlpatterns = [
    path('solo-grid/', availability_grid_view, {'mode': 'solo'}, name='solo_availability_grid'),
    path('group-grid/', availability_grid_view, {'mode': 'group'}, name='group_availability_grid'),
]
