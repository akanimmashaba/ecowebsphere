from django.shortcuts import render
from django.views.generic import ListView, CreateView,UpdateView,DeleteView
from .models import Accomodation, Address
from django.db.models import Q
from hitcount.views import HitCountDetailView
from django.urls import reverse_lazy

from.forms import AccomodationForm


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

# class CreateAddressView(CreateView): # new
#     model = Address
#     form_class = AddressForm
#     template_name = 'Create-address.html'
#     success_url = reverse_lazy('create-accomodation')


class AccomodationList(ListView):
    model = Accomodation
    template_name = 'home.html'

class AccomodationDetail(HitCountDetailView):
    model = Accomodation
    count_hit = True
    template_name = 'accommodation-detail.html'


def HomeView(request):
    house = Accomodation.objects.all()
    context = {
        'house': house,
    }
    return render(request, 'home.html',context)
    
class SearchResultsView(ListView):
    model = Accomodation
    template_name = 'search_results.html'
    context_object_name = 'results'
    
    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = Accomodation.objects.filter(
            Q(owner__username__icontains=query)
            | Q(title__icontains=query)
            | Q(address__house_number__icontains=query)
            | Q(address__house_number__icontains=query)
            | Q(address__street_name__icontains=query)
            | Q(address__provice__icontains=query)
            | Q(address__locality__icontains=query)
            | Q(address__municipality__icontains=query)
            | Q(address__postal_code__icontains=query))
        

        return object_list