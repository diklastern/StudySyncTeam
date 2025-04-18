from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserEditForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login

@login_required
def homepage(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('dashboard')
    else:
        form = CustomUserEditForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})