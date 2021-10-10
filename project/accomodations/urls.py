from django.urls import path, include
from .views import ApplyView,SearchResultsView, AccomodationList,AccomodationDetail, AccomodationUpdateView,CreateAccomodationView, DeleteAccomodationView,CreateAddressView
from accounts.views import DashboardView




urlpatterns = [
    path('', AccomodationList.as_view(), name='home'),
    path('accomodation/<int:pk>/like/', ApplyView, name='like'),
    path('accomodation/<int:pk>/', AccomodationDetail.as_view(), name='accomodation-detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('dashboard/',DashboardView.as_view(), name='dashboard'),
    path('dashboard/address/create/', CreateAddressView.as_view(), name='create-address'),
    path('dashboard/accomodation/create/', CreateAccomodationView.as_view(), name='create-accomodation'),
    path('dashboard/accomodation/update/<int:pk>/', AccomodationUpdateView.as_view(), name='update-accomodation'),
    path('dashboard/accomodation/delete/<int:pk>/', DeleteAccomodationView.as_view(), name='delete-accomodation'),
]
