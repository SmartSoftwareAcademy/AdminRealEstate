from django.urls import path
from .views import *

urlpatterns = [
    path('list/', LeaseList.as_view(), name='lease-list'),
    path('leases/', LeaseListCreate.as_view(), name='lease-create'),
    path('detail/<int:pk>/', LeaseDetailView.as_view(), name='lease-detail'),
    path('update/<int:pk>/update/', LeaseUpdateView.as_view(), name='lease-update'),
    path('delete/<int:pk>/delete/', LeaseDeleteView.as_view(), name='lease-delete'),
]
