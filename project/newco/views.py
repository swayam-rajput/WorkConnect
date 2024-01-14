from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from .models import UserProfile,Job

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
                messages.error(request, f'Passwords do not match')
                return redirect('newco-register')
        except IntegrityError as e:
            messages.error(request, f'User {username} already exists')
            # return redirect('newco-register')
    else:
        form = UserCreationForm()
    return render(request,'newco/register.html',{'form': form})

def listings(request):
    jobs = list(Job.objects.all())
    jobs = reversed(jobs)
    return render(request,'newco/listings.html',{'jobs':jobs})
def profile(request,username):
    if User.objects.filter(username=username):
        return render(request,'newco/profile.html',{'username':username})
    else:
        return HttpResponse(f'Error: User {username} does not exist')

def addjob(request:HttpRequest):
    if request.method == 'POST':
        title = request.POST.get('job-title')
        description = request.POST.get('job_description')
        job_specification = request.POST.get('job-type')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        if title == '':
            messages.error(request,f'Enter valid information')
        else:
            user = request.user
            job_post = Job.objects.create(
                user=user,
                title=title,
                description=description,
                job_specification=job_specification.upper(),
                salary=salary,
                location=location
            )
            messages.success(request,f'Posted Job')
        return redirect('newco-posted')
        return redirect('newco-add-job')
        # redirect to the jobs posted page to view the posted job and display the message there
    return render(request,'newco/addjob.html')

def posts(request):
    job = Job.objects.filter(user=request.user)
    job = reversed(job)
    return render(request,'newco/postedjobs.html',{'jobs':job})

def delete_job(request:HttpRequest,job_id):
    if request.method == 'GET':
        job = Job.objects.filter(id=int(job_id))
        job.delete()
        messages.success(request,f'Deleted job successfully')
        return redirect('newco-posted')
    