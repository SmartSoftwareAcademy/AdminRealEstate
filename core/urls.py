from django.urls import path
from .views import *
from tenants import views

urlpatterns = [
    path('user/home/',Home.as_view(),name='home'),
    path('',FrontPage.as_view(),name='frontpage'),
     path('property_page/',PropertyPage.as_view(),name='property_page'),
    path('services/',ServicePage.as_view(),name='services'),
    path('about/',AbouttPage.as_view(),name='about'),
    path('contact/',ContactPage.as_view(),name='contact'),
    path('testimony/',TestimonyView.as_view(),name='testimony'),
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='home_property-detail'),
    path('unit/<int:pk>/', UnitDetailView.as_view(), name='home_unit-detail'),
    path('add_testimonial/', TestimonialCreateView.as_view(), name='testimonial-add'),
]
