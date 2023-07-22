from django.urls import path
from .views import *

urlpatterns = [
    path('list/', StaffList.as_view(), name='staff-list'),
    path('staff/', StaffCreate.as_view(), name='staff-create'),
    path('detail/<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    path('update/<int:pk>/update/', StaffUpdateView.as_view(), name='staff-update'),
    path('delete/<int:pk>/delete/', StaffDeleteView.as_view(), name='staff-delete'),
]
