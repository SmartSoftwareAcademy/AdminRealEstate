from datetime import date

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

from tenants.models import Tenant
from staff.models import Staff


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Who is the current user ?
        # if user.is_authenticated:
        #     return redirect('home')
        # else:
        #     return redirect('login')


class DemoDataSeedMiddleware(MiddlewareMixin):
    """
    Seed a small set of demo users for the Kenyan real estate roles + tenants.
    Runs only when there are no Staff and Tenant records yet.
    """

    def process_request(self, request):
        User = get_user_model()

        # Only seed once, when there is at least one superuser
        # and there are no staff/tenant records yet.
        if not User.objects.filter(is_superuser=True).exists():
            return
        if Staff.objects.exists() or Tenant.objects.exists():
            return

        superuser = User.objects.filter(is_superuser=True).first()

        def create_demo_user(email, first_name, last_name, user_type, gender="Male", address="Nairobi, Kenya"):
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "user_type": user_type,
                    "gender": gender,
                    "address": address,
                },
            )
            if created:
                user.set_password("Pass@1234")
                user.save()
            return user

        # Property Manager
        pm_user = create_demo_user(
            email="manager.demo@estate.ke",
            first_name="Property",
            last_name="Manager",
            user_type="3",
        )
        Staff.objects.get_or_create(
            user=pm_user,
            defaults={
                "created_by": superuser,
                "mobile_number": "0725636965",
                "national_id": "30000001",
                "position": "Property Manager",
                "date_of_joining": date.today(),
            },
        )

        # Facility Manager
        fm_user = create_demo_user(
            email="facility.demo@estate.ke",
            first_name="Facility",
            last_name="Manager",
            user_type="3",
        )
        Staff.objects.get_or_create(
            user=fm_user,
            defaults={
                "created_by": superuser,
                "mobile_number": "0743793901",
                "national_id": "30000002",
                "position": "Facility Manager",
                "date_of_joining": date.today(),
            },
        )

        # Caretaker / Maintenance Technician
        ct_user = create_demo_user(
            email="caretaker.demo@estate.ke",
            first_name="Estate",
            last_name="Caretaker",
            user_type="3",
        )
        Staff.objects.get_or_create(
            user=ct_user,
            defaults={
                "created_by": superuser,
                "mobile_number": "0725000001",
                "national_id": "30000003",
                "position": "Caretaker / Maintenance Technician",
                "date_of_joining": date.today(),
            },
        )

        # Security & Groundskeeping
        sec_user = create_demo_user(
            email="security.demo@estate.ke",
            first_name="Security",
            last_name="TeamLead",
            user_type="3",
        )
        Staff.objects.get_or_create(
            user=sec_user,
            defaults={
                "created_by": superuser,
                "mobile_number": "0725000002",
                "national_id": "30000004",
                "position": "Security & Groundskeeping",
                "date_of_joining": date.today(),
            },
        )

        # Demo tenants
        # Tenant 1
        t1_user = create_demo_user(
            email="tenant1.demo@estate.ke",
            first_name="Jane",
            last_name="Tenant",
            user_type="4",
            gender="Female",
        )
        Tenant.objects.get_or_create(
            user=t1_user,
            defaults={
                "created_by": pm_user,
                "mobile_number": "0725636965",
                "National_ID": "40000001",
            },
        )

        # Tenant 2
        t2_user = create_demo_user(
            email="tenant2.demo@estate.ke",
            first_name="John",
            last_name="Tenant",
            user_type="4",
            gender="Male",
        )
        Tenant.objects.get_or_create(
            user=t2_user,
            defaults={
                "created_by": pm_user,
                "mobile_number": "0743793901",
                "National_ID": "40000002",
            },
        )
