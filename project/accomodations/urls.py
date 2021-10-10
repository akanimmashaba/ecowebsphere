from django.urls import path, include
from .views import Dashboard, SearchResultsView, AccomodationList,AccomodationDetail, AccomodationUpdateView,CreateAccomodationView, DeleteAccomodationView

urlpatterns = [
    # path('', HomeView, name='home'),
    path('', AccomodationList.as_view(), name='home'),
    # path('accomodation/<slug:slug>/', AccomodationDetail.as_view(), name='accomodation-detail'),
    path('accomodation/<int:pk>/', AccomodationDetail.as_view(), name='accomodation-detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('dashboard/', Dashboard, name='dashboard'),
    path('dashboard/create/', CreateAccomodationView.as_view(), name='create-accomodation'),
    path('dashboard/update/<int:pk>/', AccomodationUpdateView.as_view(), name='update-accomodation'),
    path('dashboard/delete/<int:pk>/', DeleteAccomodationView.as_view(), name='delete-accomodation'),
]
