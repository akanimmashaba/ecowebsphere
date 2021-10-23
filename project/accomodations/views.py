from django.shortcuts import redirect, render,get_object_or_404
from django.urls.base import reverse
from django.views.generic import ListView, CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from .models import Accomodation,Address, Application
# from accounts.models import Profile
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import AccomodationForm, AddressForm
from django.http import HttpResponseRedirect, request
from django.utils import timezone
from django.http import request



class CreateAccomodationView(CreateView):
    model = Accomodation
    form_class = AccomodationForm
    template_name = 'Create-accomodation.html'
    success_url = reverse_lazy('dashboard')

class DeleteAccomodationView(DeleteView):
    model = Accomodation
    template_name = 'delete-accomodation.html'
    success_url = reverse_lazy('my-accomodations')

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

def AccomodationsList(request):
    context = {
        'object': Accomodation.objects.all()
    }
    return render(request, 'accomodation-list.html', context)

@login_required
def MyAccomodations(request):
    context = {
        'accomodations': Accomodation.objects.all().filter(owner=request.user)
    }
    return render(request, 'my-accomodations.html', context)

@login_required
def ViewReport(request, pk):
    accomodation = get_object_or_404(Accomodation, pk=pk)
    # accomodation_applications as accom_apps
    applied_accomodations = accomodation.applied.all()
    
        
    context = {
        'applied_accomodations':applied_accomodations,
    }
    return render(request, 'report-page.html', context)

class ApplicationDetail(DetailView):
    model = Application
    template_name = 'applications.html'

@login_required
def Apply(request, pk):
    accomodation =  get_object_or_404(Accomodation, id=request.POST.get('accomodation_id'))
    applied = False
    if Accomodation.applied.filter(id=request.user.id).exists():
        accomodation.applied.remove(request.user)
        applied = False
    else:
        accomodation.applied.add(request.user)
        applied = True
    return HttpResponseRedirect(reverse('accomodation-detail', args=[str(pk)]))
    

class AccomodationList(ListView):
    model = Accomodation
    paginate_by = 10
    template_name = 'home.html'

class AccomodationDetail(DetailView):
    model = Accomodation
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