from django.shortcuts import render
from datetime import date

def solo_availability_view(request):
    return render(request, "availability/solo_form.html", {})

def group_availability_view(request):
    return render(request, "availability/group_form.html", {})
