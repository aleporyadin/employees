from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from authentication.forms import LoginForm


def sign_up(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your account has been created.')
        return redirect('login')
    return render(request, 'register.html', {'form': form})


def sign_in(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You have been logged in.')
            return redirect('home')
    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


def sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')
