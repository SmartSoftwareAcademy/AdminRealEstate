import json
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from .EmailBackend import EmailBackend
from django.core.files.storage import FileSystemStorage
from .forms import CustomUserForm
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.


def login_page(request):
    if request.method == 'POST':
        # Authenticate
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid details")
            return redirect("frontpage")
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, 'account/sign-in.html')


def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("frontpage")

def view_profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    form = CustomUserForm(request.POST or None, request.FILES or None,
                     instance=user)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = user
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage(location='profiles/')
                    filename = fs.save(passport.name, passport)
                    # passport_url = fs.url(filename)
                    custom_user.profile_pic =  'profiles/' + filename
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect('login')
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "account/profile.html", context)
