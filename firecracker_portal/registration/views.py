# registration/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUserProfile
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StallApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
# registration/views.py
from django.contrib.auth.decorators import login_required
from .models import StallApplication 
from django.urls import reverse
from .decorators import role_required

HOD_DEPARTMENTS = ['HOD_FIRE', 'HOD_REDCROSS', 'HOD_POLICE']

'''
    DC Based Views
'''
@login_required
@role_required(['DC'])
def dc_forward_application(request, app_id):
    application = get_object_or_404(StallApplication, id=app_id)
    application.status="Pending"
    application.save()
    messages.success(request, "Application forwarded to all HODs")
    return redirect('dc_fresh_requests')

@login_required
@role_required(['DC'])
def dc_fresh_requests(request):
    applications = StallApplication.objects.filter(
        status='Fresh'
    ).order_by('-submitted_at')

    return render(request, 'dc/dc_fresh_requests.html', {
        'applications': applications,
        'role': 'DC',
        'dashboard_type': 'Fresh Requests'
    })

@login_required
@role_required(['DC'])
def dc_pending_requests(request):
    applications = StallApplication.objects.filter(
        status='Pending'
    ).order_by('-submitted_at')

    return render(request, 'dc/dc_pending_requests.html', {
        'applications': applications,
        'role': 'DC',
        'dashboard_type': 'Pending Requests'
    })

@login_required
@role_required(['DC'])
def dc_finalize_requests(request):
    applications = StallApplication.objects.filter(
        hod_fire_approval_doc__isnull=False,
        hod_police_approval_doc__isnull=False,
        hod_redcross_approval_doc__isnull=False,
        hod_fire_status='Verified',
        hod_police_status="Verified",
        hod_redcross_status="Verified",
        status='Pending'
    ).order_by('-submitted_at')

    return render(request, 'dc/dc_finalize_request.html', {
        'applications': applications,
        'role': 'DC',
        'dashboard_type': 'Finalize Requests'
    })

@login_required
@role_required(['DC'])
def dc_dashboard(request):
    applications = StallApplication.objects.all().order_by('-submitted_at')
    return render(request, 'dc/dc_dashboard.html', {'applications': applications})


@login_required
@role_required(['DC'])
def approve_application(request, app_id):
    app = get_object_or_404(StallApplication, id=app_id)
    app.status = 'Verified'
    app.save()
    return redirect('dc_dashboard')

@login_required
@role_required(['DC'])
def reject_application(request, app_id):
    app = get_object_or_404(StallApplication, id=app_id)
    app.status = 'Rejected'
    app.save()
    return redirect('dc_dashboard')


@login_required
def stall_registration(request):
    if request.method == 'POST':
        form = StallApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = get_object_or_404(CustomUserProfile, email=request.user)
            application.save()
            messages.success(request, "Stall registered successfully!")
            return redirect('stall_registration')
    else:
        form = StallApplicationForm()
    return render(request, 'stall_registration.html', {'form': form})

def generate_otp():
    return str(random.randint(100000, 999999))

def register_user(request):
    otp_sent = False
    user = None
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_input = request.POST.get('otp')
        try:
            user = CustomUserProfile.objects.get(email=email)
        except:
            pass

        # OTP Verification Flow
        if otp_input:
            if user and user.otp == otp_input:
                # Check if OTP is expired
                if timezone.now() - user.otp_created_at > timedelta(seconds=300):
                    messages.error(request, "OTP has expired. Please request a new one.")
                    user.otp = None
                    user.otp_created_at = None
                    user.save()
                    otp_sent = False
                else:
                    user.is_verified = True
                    user.otp = None
                    user.otp_created_at = None
                    user.failed_attempts = 0
                    user.save()
                    # Create session for the authenticated user
                    login(request, user)
                    messages.success(request, "OTP verified successfully!")
                    return redirect('stall_registration')
            else:
                if user:
                    user.failed_attempts += 1
                    if user.failed_attempts >= 3:
                        user.is_locked = True
                        messages.error(request, "Account locked due to 3 failed attempts.")
                    else:
                        messages.error(request, f"Incorrect OTP. Attempt {user.failed_attempts}/3.")
                    user.save()
                else:
                    messages.error(request, "User not found.")
                otp_sent = True

        # Registration or Resend OTP Flow
        else:
            if not user:
                first_name = request.POST.get('first_name', '')
                last_name = request.POST.get('last_name', '')
                # create a new user record populated from the form (password managed via OTP flow)
                user = CustomUserProfile(
                    email=email,
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    is_verified=False
                )
                if hasattr(user, 'set_unusable_password'):
                    user.set_unusable_password()
            if user.is_locked:
                messages.error(request, "Account is locked. Please contact admin.")
            else:
                otp = generate_otp()
                user.otp = otp
                user.otp_created_at = timezone.now()
                user.failed_attempts = 0
                user.save()
                send_mail(
                    'Your OTP for Firecracker Stall Registration',
                    f'Your OTP is: {otp}',
                    'noreply@firecracker.com',
                    [email],
                    fail_silently=False,
                )
                messages.info(request, "OTP sent to your email.")
                otp_sent = True


    return render(request, 'register.html', {'otp_sent': otp_sent, 'user':user})

#dc login
def dc_login(request):
    otp_sent = False
    user = None
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_input = request.POST.get('otp')
        try:
            user = CustomUserProfile.objects.get(email=email)
        except:
            return redirect('unauthorized')

        # OTP Verification Flow
        if otp_input:
            if user and user.otp == otp_input:
                # Check if OTP is expired
                if timezone.now() - user.otp_created_at > timedelta(seconds=300):
                    messages.error(request, "OTP has expired. Please request a new one.")
                    user.otp = None
                    user.otp_created_at = None
                    user.save()
                    otp_sent = False
                else:
                    user.is_verified = True
                    user.otp = None
                    user.otp_created_at = None
                    user.failed_attempts = 0
                    user.save()
                    
                    messages.success(request, "OTP verified successfully!")
                    # if the verified user is a DC, send them to the DC dashboard
                    if getattr(user, 'role', '').upper() == 'DC':
                        # Create session for the authenticated user
                        login(request, user)
                        return redirect('dc_dashboard')
                    return redirect('unauthorized')
            else:
                if user:
                    user.failed_attempts += 1
                    if user.failed_attempts >= 3:
                        user.is_locked = True
                        messages.error(request, "Account locked due to 3 failed attempts.")
                    else:
                        messages.error(request, f"Incorrect OTP. Attempt {user.failed_attempts}/3.")
                    user.save()
                else:
                    messages.error(request, "User not found.")
                otp_sent = True
    

        # Registration or Resend OTP Flow
        else:
            if user.is_locked:
                messages.error(request, "Account is locked. Please contact admin.")
            else:
                otp = generate_otp()
                user.otp = otp
                user.otp_created_at = timezone.now()
                user.failed_attempts = 0
                user.save()
                send_mail(
                    'Your OTP for Account Login',
                    f'Your OTP is: {otp}',
                    'noreply@firecracker.com',
                    [email],
                    fail_silently=False,
                )
                messages.info(request, "OTP sent to your email.")
                otp_sent = True 
    return render(request, 'dc/dc_login.html', {'otp_sent': otp_sent, 'user':user})

#hod login
def hod_login(request):
    otp_sent = False
    user = None
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_input = request.POST.get('otp')
        try:
            user = CustomUserProfile.objects.get(email=email)
        except:
            return redirect('unauthorized')

        # OTP Verification Flow
        if otp_input:
            if user and user.otp == otp_input:
                # Check if OTP is expired
                if timezone.now() - user.otp_created_at > timedelta(seconds=300):
                    messages.error(request, "OTP has expired. Please request a new one.")
                    user.otp = None
                    user.otp_created_at = None
                    user.save()
                    otp_sent = False
                else:
                    user.is_verified = True
                    user.otp = None
                    user.otp_created_at = None
                    user.failed_attempts = 0
                    user.save()
                    
                    messages.success(request, "OTP verified successfully!")
                    # if the verified user is a DC, send them to the DC dashboard
                    if getattr(user, 'role', '').upper() in ['HOD_FIRE', 'HOD_REDCROSS', 'HOD_POLICE']:
                        # Create session for the authenticated user
                        login(request, user)
                        return redirect('hod_dashboard')
                    return redirect('unauthorized')
            else:
                if user:
                    user.failed_attempts += 1
                    if user.failed_attempts >= 3:
                        user.is_locked = True
                        messages.error(request, "Account locked due to 3 failed attempts.")
                    else:
                        messages.error(request, f"Incorrect OTP. Attempt {user.failed_attempts}/3.")
                    user.save()
                else:
                    messages.error(request, "User not found.")
                otp_sent = True
    

        # Registration or Resend OTP Flow
        else:
            if user.is_locked:
                messages.error(request, "Account is locked. Please contact admin.")
            else:
                otp = generate_otp()
                user.otp = otp
                user.otp_created_at = timezone.now()
                user.failed_attempts = 0
                user.save()
                send_mail(
                    'Your OTP for Account Login',
                    f'Your OTP is: {otp}',
                    'noreply@firecracker.com',
                    [email],
                    fail_silently=False,
                )
                messages.info(request, "OTP sent to your email.")
                otp_sent = True

    return render(request, 'hod/hod_login.html', {'otp_sent': otp_sent, 'user':user})

'''
    2. HOD Based Views
'''
@login_required
@role_required(HOD_DEPARTMENTS)
def hod_dashboard(request):
    try:
        profile = CustomUserProfile.objects.get(username=request.user)
        role, full_name = [(role, full_name) for (role, full_name) in profile.ROLE_CHOICES if role == profile.role][0]
    except:
        return redirect('unauthorized')
    applications = StallApplication.objects.all().order_by('-submitted_at')
    return render(request, 'hod/hod_dashboard.html', {'applications': applications, 'role':full_name})

@login_required
@role_required(HOD_DEPARTMENTS)
def process_application(request, app_id):
    application = get_object_or_404(StallApplication, id=app_id)
    user = request.user
    profile = CustomUserProfile.objects.get(username=user)
    (role, full_name) = [(role, full_name) for (role, full_name) in profile.ROLE_CHOICES if role == profile.role][0]
    # Map role to fields
    role_fields = {
        'DC': ('dc_comment', 'dc_approval_doc', 'dc_status'),
        'HOD_FIRE': ('hod_fire_comment', 'hod_fire_approval_doc', 'hod_fire_status'),
        'HOD_REDCROSS': ('hod_redcross_comment', 'hod_redcross_approval_doc', 'hod_redcross_status'),
        'HOD_POLICE': ('hod_police_comment', 'hod_police_approval_doc', 'hod_police_status'),
    }

    comment_field, doc_field, status_field = role_fields[role]

    if request.method == 'POST':
        comment = request.POST.get('comment')
        approval_doc = request.FILES.get('approval_doc')
        status = request.POST.get('status')
        setattr(application, comment_field, comment)
        setattr(application, status_field, status)
        if approval_doc:
            setattr(application, doc_field, approval_doc)

        application.save()
        messages.success(request, "Review submitted successfully.")
        return redirect('hod_dashboard')  # or role-specific dashboard

    return render(request, 'hod/process_application.html', {
        'application': application,
        'role': full_name
    })