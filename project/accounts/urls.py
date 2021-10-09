from django.urls import path,include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import signup

urlpatterns = [
    path('signup/', signup, name="signup"),
    
]