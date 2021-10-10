from django.shortcuts import render,get_object_or_404
from django.urls.base import reverse
from django.views.generic import ListView, CreateView,UpdateView,DeleteView
from .models import Accomodation,Address
from accounts.models import Profile
from django.db.models import Q
from hitcount.views import HitCountDetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import AccomodationForm, AddressForm
from django.http import HttpResponseRedirect
User = get_user_model()

@login_required
def ApplyView(request, pk):
    accomodation =  get_object_or_404(Accomodation, id=request.POST.get('accomodation_id'))
    accomodation.like.add(request.user)
    return HttpResponseRedirect(reverse('home', args=[str(pk)]))

class CreateAccomodationView(CreateView):
    model = Accomodation
    form_class = AccomodationForm
    template_name = 'Create-accomodation.html'
    success_url = reverse_lazy('home')

class DeleteAccomodationView(DeleteView):
    model = Accomodation
    success_url = reverse_lazy('home')

class AccomodationUpdateView(UpdateView):
    model = Accomodation
    form_class = AccomodationForm
    template_name = 'update-accomodation.html'

class CreateAddressView(CreateView): # new
    model = Address
    form_class = AddressForm
    template_name = 'Create-address.html'
    success_url = reverse_lazy('create-accomodation')

class AccomodationCreateView(CreateView):
    model = Accomodation
    template_name = "Create-accomodation.html"

class AccomodationList(ListView):
    model = Accomodation
    template_name = 'home.html'

class AccomodationDetail(HitCountDetailView):
    model = Accomodation
    count_hit = True
    template_name = 'accommodation-detail.html'


class SearchResultsView(ListView):
    model = Accomodation
    template_name = 'search_results.html'
    context_object_name = 'results'
    
    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = Accomodation.objects.filter(
            Q(title__icontains=query)
            | Q(address__house_number__icontains=query)
            | Q(address__house_number__icontains=query)
            | Q(address__street_name__icontains=query)
            | Q(address__provice__icontains=query)
            | Q(address__locality__icontains=query)
            | Q(address__municipality__icontains=query)
            | Q(address__postal_code__icontains=query))
        

        return object_list