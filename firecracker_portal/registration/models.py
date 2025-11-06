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
    STATUS_CHOICES = [
        ('Fresh','Fresh'),
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected')
    ]
    user = models.ForeignKey(CustomUserProfile, on_delete=models.CASCADE)
    stall_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Fresh')

# PDF upload field
    document = models.FileField(upload_to='documents/', blank=True, null=True)
#  Departmental review fields
    dc_comment = models.TextField(blank=True, null=True)
    dc_approval_doc = models.FileField(upload_to='approvals/dc/', blank=True, null=True)

    hod_fire_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    hod_fire_comment = models.TextField(blank=True, null=True)
    hod_fire_approval_doc = models.FileField(upload_to='approvals/fire/', blank=True, null=True)

    hod_redcross_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    hod_redcross_comment = models.TextField(blank=True, null=True)
    hod_redcross_approval_doc = models.FileField(upload_to='approvals/redcross/', blank=True, null=True)

    hod_police_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    hod_police_comment = models.TextField(blank=True, null=True)
    hod_police_approval_doc = models.FileField(upload_to='approvals/police/', blank=True, null=True)

    def __str__(self):
        return f"{self.stall_name} ({self.user.email})"

