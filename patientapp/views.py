from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from django.contrib import messages
from datetime import date

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import *
from .models import *
from django.contrib import messages, auth
import datetime
from re import split
from .doctorchoices import category, fromTimeChoice, toTimeChoice
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

def home(request):
    card_list = Card.objects.all()  

    context = {
        'card_list': card_list
    }

    return render(request, 'home.html', context)

def customerregister(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('login')
                    
    else:
        form = RegistrationForm()
    
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)

from django.contrib.auth import authenticate, login as auth_login  # Rename the login function

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)  # Use the renamed auth_login function
            current_user = Account.objects.get(id=request.user.id)
            if not Customer.objects.filter(user=current_user).exists():
                customer = Customer(user=current_user)
                customer.save()

            return redirect('customer_dashboard')

        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'users/login.html')



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('home')


def customers_profile(request):
    current_user = request.user
    current_customer = Customer.objects.get(user=current_user)

    if request.method == 'POST' and current_user.is_authenticated:
        form = CustomerForm(request.POST, request.FILES, instance=current_customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.age_years = calculate_age_years(customer.date_of_birth)
            customer.save()  
            return redirect('customer_dashboard')
    else:
        form = CustomerForm(instance=current_customer)

    context = {
        'customer': current_customer,
        'form': form,
    }
    return render(request, 'patients/patients-profile.html', context)

def calculate_age_years(date_of_birth):
    today = date.today()
    if date_of_birth:
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
    return None

