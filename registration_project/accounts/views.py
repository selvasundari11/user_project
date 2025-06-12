from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import UserProfile
from .forms import RegistrationForm, LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if 'signup' in request.POST:
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                try:
                    user = UserProfile.objects.get(email=email)
                    if check_password(password, user.password):
                        # Login successful
                        request.session['user_id'] = user.id
                        return redirect('welcome')
                    else:
                        messages.error(request, 'Invalid password.')
                except UserProfile.DoesNotExist:
                    messages.error(request, 'New Users register first and signup the form.')
                    #return redirect('register')
        #elif 'register' in request.POST:
            #return redirect('register')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    success_message = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # This saves to your MSSQL DB via Django ORM
            success_message = "Registration successful!"
            form = RegistrationForm()  # Reset form after success
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {
        'form': form,
        'success_message': success_message,
    })


def welcome_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = UserProfile.objects.get(id=user_id)
    return render(request, 'accounts/welcome.html', {'user': user})
