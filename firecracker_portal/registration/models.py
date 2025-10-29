# registration/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Custom User
class CustomUserProfile(User):
    ROLE_CHOICES = [
        ('DC', 'District Commissioner'),
        ('HOD_FIRE', 'HOD - Fire Department'),
        ('HOD_REDCROSS', 'HOD - Red Cross'),
        ('HOD_POLICE', 'HOD - Police Department'),
        ('USER', 'Regular User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)  # Add this
    is_verified = models.BooleanField(default=False)
    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    
# registration/models.py
class StallApplication(models.Model):
    user = models.ForeignKey(CustomUserProfile, on_delete=models.CASCADE)
    stall_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected')
    ], default='Pending')



    def __str__(self):
        return f"{self.stall_name} ({self.user.email})"


