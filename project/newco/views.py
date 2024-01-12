from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from .models import UserProfile

# Create your views here.
def log_in(request,user_name=None,psd=None):
    if request.method == 'POST':   
        # username = request.POST['username']
        # password = request.POST['password']
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f'User {username} logged in')
            return redirect('newco-home')
        else:
            messages.error(request,f'Invalid credentials')
    return render(request,'newco/login.html')


def log_out(request:HttpRequest):
    """Logs out the user associated with the request object"""
    username = request.user.get_username()
    logout(request)
    messages.success(request,f'User {username} logged out')
    return redirect('newco-login')
    
def homepage(request):
    # if not request.user.is_authenticated:
    #     return redirect('newco-login')
        
    return render(request,'newco/home.html')
    
def register(request):
    """Register users directly to django admin"""
    # dont forget to automatically login the registered user
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        phno = request.POST.get('phno')
        age = request.POST.get('age')
        gender = request.POST.get('radio')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        try:
            if password == cpassword:
                user = User.objects.create_user(username=username, email=email, password=password)
                user_profile = UserProfile.objects.create(user=user, age=age, phno=phno, gender=gender)
                user_profile.save()
                messages.success(request, f'User {username} registered')
                return redirect('newco-home')
            else:
                messages.error(request, f'Enter valid information')
                return redirect('newco-register')
        except IntegrityError as e:
            messages.error(request, f'User {username} already exists')
            # return redirect('newco-register')
        except ValueError as e:
            pass
    else:
        form = UserCreationForm()
    return render(request,'newco/register.html',{'form': form})

def listings(request):
    return render(request,'newco/listings.html')

