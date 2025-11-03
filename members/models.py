import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Member(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # <- have to Use this instead of User
        on_delete=models.CASCADE
        )
    name = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to="profilepic/", blank=True, null=True)
    office_id = models.CharField(unique=True, max_length=50, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    MEMBERSHIP_CHOICES = [
        ('T', 'Teacher'),
        ('S', 'Student'),
        ('ST', 'Staff'),
        ('O', 'Other'),
    ]
    membership_type = models.CharField(max_length=2, choices=MEMBERSHIP_CHOICES)
    

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    
#next step -> Create profile automatically when a new user registers - signals.py
