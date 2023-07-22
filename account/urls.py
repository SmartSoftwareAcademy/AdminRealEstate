from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login_page, name='login'),
    path("logout_user/", logout_user, name='logout'),
    path("user/profile", view_profile,name='profile'),
]
