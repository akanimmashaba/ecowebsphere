from django.urls import path, include
from .views import SearchResultsView, AccomodationList,AccomodationDetail, HomeView

urlpatterns = [
    path('', HomeView, name='home'),
    # path('accomodation/<slug:slug>/', AccomodationDetail.as_view(), name='accomodation-detail'),
    path('accomodation/<int:pk>/', AccomodationDetail.as_view(), name='accomodation-detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]
