from django.urls import path
from .views import *


urlpatterns = [
    # Property Owner URLs
    path('owners/', PropertyOwnerList.as_view(), name='owner_list'),
    path('owners/<int:pk>/', PropertyOwnerDetail.as_view(), name='owner_detail'),

    # Agent URLs
    path('agents/', AgentList.as_view(), name='agent-list'),
    path('agents/<int:pk>/', AgentDetail.as_view(), name='agent-detail'),

    ]