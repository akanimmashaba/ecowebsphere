from django.urls import path, include
from .views import (
    # ApplyView,
    Apply,
    SearchResultsView,
    AccomodationList,
    AccomodationDetail, 
    AccomodationUpdateView,
    CreateAccomodationView, 
    DeleteAccomodationView,
    CreateAddressView,
    MyAccomodations,
    AccomodationsList,
    ViewReport,

)

from accounts.views import DashboardView,profileView

app_name = 'accomodation'


urlpatterns = [
    path('', AccomodationList.as_view(), name='home'),
    # path('accomodation/<int:pk>/like/', ApplyView, name='like'),
    # path('accomodation/apply/<int:pk>/', Apply, name='apply'),
    path('profile/', profileView, name='profile'),
    path('search/', SearchResultsView.as_view(), name='search_results'),

    path('accomodation/', AccomodationsList, name='accomodation-list'),
    path('accomodation/<int:pk>/', AccomodationDetail.as_view(), name='accomodation-detail'),
    # path('accomodation/<int:pk>/apply/', Apply, name='apply'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('dashboard/',DashboardView.as_view(), name='dashboard'),
    path('dashboard/address/create/', CreateAddressView.as_view(), name='create-address'),
    path('dashboard/accomodation/create/', CreateAccomodationView.as_view(), name='create-accomodation'),
    path('dashboard/accomodation/update/<int:pk>/', AccomodationUpdateView.as_view(), name='update-accomodation'),
    path('dashboard/accomodation/delete/<int:pk>/', DeleteAccomodationView.as_view(), name='delete-accomodation'),
    path('dashboard/accomodation/my-accomodations/', MyAccomodations, name='my-accomodations'),
    path('dashboard/accomodation/my-accomodations/<int:pk>/', ViewReport, name='report'),

]

