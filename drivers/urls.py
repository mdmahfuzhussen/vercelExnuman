# drivers/urls.py
from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    path('reviews/submit/', views.submit_review, name='submit_review'),
    # Signup url line has been completely removed
]