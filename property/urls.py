from django.urls import path
from .views import *


urlpatterns = [
 # Property URLs
    path('list/', PropertyList.as_view(), name='property-list'),
    path("list/<int:id>/", PropertyList.as_view(), name="property-list"),
    path("create/", PrpertyCreateView.as_view(), name="property-create"),
    path("<int:pk>/detail/", PropertyDetailView.as_view(), name="property-detail"),
    path("<int:pk>/update/", PropertyUpdateView.as_view(), name="property-update"),
    path("<int:pk>/delete/",PropertyDeleteView.as_view(), name="property-delete"),

]