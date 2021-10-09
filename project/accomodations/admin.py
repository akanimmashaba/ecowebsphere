from django.contrib import admin
from .models import Accomodation, Address, Application
# Register your models here.

admin.site.register(Accomodation)
admin.site.register(Address)
admin.site.register(Application)