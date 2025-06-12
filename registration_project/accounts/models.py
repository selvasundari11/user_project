# accounts/models.py

from django.db import models

class UserProfile(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    contact_number = models.CharField(max_length=11)  # country code + phone (3+8)
    dob = models.DateField()
    civil_id = models.CharField(max_length=12, unique=True)
    file_upload = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.full_name
