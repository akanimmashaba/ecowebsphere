from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Accomodation, Address
from django.db.models import Q
from django.views.generic.list import ListView
from hitcount.views import HitCountDetailView


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