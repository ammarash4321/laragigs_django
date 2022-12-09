from django.urls import path
from .views import HomeView, ListingsView, ListingView, LoginView, \
    LogoutView, CreateListingView, UpdateListingView, DeleteListingView, ListingChartView, RegisterView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('listings/', login_required(ListingsView.as_view()), name='listings'),
    path('listing/<int:pk>', login_required(ListingView.as_view()), name='listing'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-listing/', login_required(CreateListingView.as_view()), name='create-listing'),
    path('update-listing/<int:pk>', login_required(UpdateListingView.as_view()), name='update-listing'),
    path('delete-listing/<int:pk>', login_required(DeleteListingView.as_view()), name='delete-listing'),
    path('listing-chart/', login_required(ListingChartView.as_view()), name='listing-chart'),
]