# accounts/forms.py

from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import datetime
import re



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    country_code = forms.CharField(max_length=3, min_length=3, label="Country Code")
    phone_number = forms.CharField(max_length=8, min_length=8, label="Phone Number")
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    file_upload = forms.FileField(label="Upload File")

    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'password', 'confirm_password', 'country_code', 'phone_number', 'dob', 'civil_id', 'file_upload']

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[A-Za-z ]+$', full_name):
            raise ValidationError("Full Name must contain only letters and spaces.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        dob = cleaned_data.get("dob")
        if dob:
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if dob > today:
                self.add_error('dob', "Date of Birth cannot be in the future.")
            elif age < 18:
                self.add_error('dob', "You must be at least 18 years old.")

        country_code = cleaned_data.get("country_code")
        phone_number = cleaned_data.get("phone_number")
        if country_code and (not country_code.isdigit() or len(country_code) != 3):
            self.add_error('country_code', "Country code must be 3 digits.")
        if phone_number and (not phone_number.isdigit() or len(phone_number) != 8):
            self.add_error('phone_number', "Phone number must be 8 digits.")

        civil_id = cleaned_data.get("civil_id")
        if civil_id and (not civil_id.isdigit() or len(civil_id) != 12):
            self.add_error('civil_id', "Civil ID must be exactly 12 digits.")
            
    def clean_civil_id(self):
        civil_id = self.cleaned_data.get('civil_id')
        if UserProfile.objects.filter(civil_id=civil_id).exists():
            raise ValidationError("This Civil ID is already in use.")
        return civil_id
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Combine country code and phone number
        user.contact_number = self.cleaned_data['country_code'] + self.cleaned_data['phone_number']
        # Hash the password before saving
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    



class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    
   


