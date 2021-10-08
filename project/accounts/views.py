from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.views import LoginView  


class Login(LoginView):
    template_name = 'registration/login.html'

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.refresh_from_db()
            request.user.profile.first_name = form.cleaned_data.get('first_name')
            request.user.profile.last_name = form.cleaned_data.get('last_name')
            request.user.profile.dob = form.cleaned_data.get('dob')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

