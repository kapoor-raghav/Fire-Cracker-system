# registration/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def register_user(request):
    otp_sent = False

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        otp_input = request.POST.get('otp')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            user = None

        # OTP Verification Flow
        if otp_input:
            if user and user.otp == otp_input:
                # Check if OTP is expired
                if timezone.now() - user.otp_created_at > timedelta(seconds=15):
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
                user = UserProfile(full_name=full_name, email=email)
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

    return render(request, 'register.html', {'otp_sent': otp_sent})
