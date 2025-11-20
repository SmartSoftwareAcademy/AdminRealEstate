from django.urls import path
from .views import *

urlpatterns = [
    path('tenants/', TenatList.as_view(), name='tenant-list'),
    # Tenant self-service profile (for logged-in tenants)
    path('me/', TenantSelfDetailView.as_view(), name='tenant-me'),
    path("create/", TenantCreateView.as_view(), name="tenant-create"),
    path("<int:pk>/detail/", TenantDetailView.as_view(), name="tenant-detail"),
    path("<int:pk>/update/", TenantUpdateView.as_view(), name="tenant-update"),
    path("<int:pk>/delete/",TenantDeleteView.as_view(), name="tenant-delete"),

]
