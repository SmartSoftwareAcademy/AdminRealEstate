from django.urls import path
from .views import *

urlpatterns = [
    path('notice/create/', NoticeView.as_view(), name='notice_add'),
    path('notice/detail/<int:pk>/', NoticeDetail.as_view(), name='notice-detail'),
]


