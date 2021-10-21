from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from accomodations.models import Accomodation


from .forms import ProfileForm
from .models import Profile
from accounts.admin import UserCreationForm, UserChangeForm


class Login(LoginView):
    template_name = 'registration/login.html'

class Logout(LogoutView):
    template_name = 'registration/logout.html'

# def signup(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         profile_form = ProfileForm(instance=request.user,data=request.POST)
#         if form.is_valid() and profile_form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             user.profile.first_name = form.cleaned_data.get('first_name')
#             user.profile.last_name = form.cleaned_data.get('last_name')
#             user.profile.email = form.cleaned_data.get('email')
#             user.save()
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})

# def signup(request):
#     user = request.user
#     form = UserCreationForm(request.POST)
#     profile = ProfileForm()
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         profile_form = profile(request.POST)
#         if form.is_valid() :
#             user = form.save(commit=False)
#             user.save()
#             user = form.save()
#             user.refresh_form_db()
#             user.profile.user_type = form.cleaned_data.get('user_type')
#             user.save()
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#         profile = ProfileForm()

#     return render(request, 'registration/signup.html', {'form': form})


def signup(request):
    user = request.user
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(View):
    profile = None
    success_url = reverse_lazy('dashbord')
    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        accomodations = Accomodation.objects.all().filter(owner=request.user)
        context = {
            'profile': self.profile,
            'accomodations': accomodations
        }
        return render(request, 'dashboard.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)
        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            form = ProfileForm()
        return redirect('dashboard')


def profileView(request):
    user_form = UserChangeForm
    profile_form = ProfileForm
    if request.method == request.POST:
        form_1 = user_form(request.POST, instance=request.user)
        form_2 = profile_form(request.Post, instance=request.user.profile)

        if form_1.is_valid() and form_2.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='dashboard')

        else:
            user_form = UserChangeForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'edit-profile.html', context)

