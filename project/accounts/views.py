from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


from .forms import ProfileForm
from .models import Profile
from .forms import CustomUserCreationForm


class Login(LoginView):
    template_name = 'registration/login.html'

class Logout(LogoutView):
    template_name = 'registration/logout.html'

def signup(request):
    user_ = request.user
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user_.refresh_from_db()
            user_.profile.first_name = form.cleaned_data.get('first_name')
            user_.profile.last_name = form.cleaned_data.get('last_name')
            user_.profile.dob = form.cleaned_data.get('dob')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(View):
    profile = None
    success_url = reverse_lazy('dashbord')
    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'profile': self.profile,
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

