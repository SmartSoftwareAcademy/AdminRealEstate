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
        if user is not None:
            login(request, user)
            # Role-aware landing after login
            # Tenants land on their dashboard (home has tenant analytics/notice board)
            # Other roles land on the main admin/owner/agent dashboard
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
    
    # Get related data based on user type
    related_data = {}
    if user.user_type == '4':  # Tenant
        try:
            from tenants.models import Tenant
            related_data['tenant'] = Tenant.objects.filter(user=user).first()
        except:
            pass
    elif user.user_type == '3':  # Staff
        try:
            from staff.models import Staff
            related_data['staff'] = Staff.objects.filter(user=user).first()
        except:
            pass
    elif user.user_type == '2':  # Agent
        try:
            from landlords.models import Agent
            related_data['agent'] = Agent.objects.filter(user=user).first()
        except:
            pass
    elif user.user_type == '1':  # Owner
        try:
            from landlords.models import PropertyOwner
            related_data['owner'] = PropertyOwner.objects.filter(user=user).first()
        except:
            pass
    
    context = {
        'form': form,
        'page_title': 'View/Edit Profile',
        'user': user,
        **related_data
    }
    
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                other_name = form.cleaned_data.get('other_name', '')
                email = form.cleaned_data.get('email')
                gender = form.cleaned_data.get('gender')
                address = form.cleaned_data.get('address', '')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                
                custom_user = user
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage(location='profiles/')
                    filename = fs.save(passport.name, passport)
                    custom_user.profile_pic = 'profiles/' + filename
                
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.other_name = other_name
                custom_user.email = email
                custom_user.gender = gender
                custom_user.address = address
                custom_user.save()
                
                messages.success(request, "Profile Updated Successfully!")
                if password:
                    messages.info(request, "Please login again with your new password.")
                    return redirect('login')
                else:
                    return redirect('profile')
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occurred While Updating Profile: " + str(e))
    return render(request, "account/profile.html", context)
