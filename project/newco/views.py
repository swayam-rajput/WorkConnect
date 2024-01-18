from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpRequest
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from .models import UserProfile,Job

# Create your views here.
def custom_404(request,exception):
    return render(request, 'newco/404.html')

def log_in(request,user_name=None,psd=None):
    if request.method == 'POST':   
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

@login_required
def homepage(request):
    if not request.user.is_authenticated:
        return redirect('newco-login')
        
    return render(request,'newco/home.html')
    
def register(request):
    """Register users directly to django admin"""
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
                return redirect('newco-login')
            else:
                messages.error(request, f'Passwords do not match')
        except IntegrityError as e:
            messages.error(request, f'User {username} already exists')
            
    else:
        form = UserCreationForm()
    return render(request,'newco/register.html',{'form': form})

@login_required
def listings(request):
    jobs = Job.objects.all()
    jobs = reversed(jobs)
    return render(request,'newco/listings.html',{'jobs':jobs})

    
@login_required
def addjob(request:HttpRequest):
    """Creates a new job based on the information provided via the form"""
    if request.method == 'POST':
        title = request.POST.get('job-title')
        description = request.POST.get('job_description')
        job_spec = request.POST.get('job-type')
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
                job_specification=job_spec.upper(),
                salary=salary,
                location=location
            )
            messages.success(request,f'Posted Job')
        return redirect('newco-posted')
        # redirect to the jobs posted page to view the posted job and display the message there
    return render(request,'newco/addjob.html')

@login_required
def posts(request):
    job = Job.objects.filter(user=request.user)
    if job.count() == 0:
        job = None
    else:
        job = reversed(job)
    return render(request,'newco/postedjobs.html',{'jobs':job})

@login_required
def delete_job(request:HttpRequest,job_id):
    if request.method == 'GET':
        job = Job.objects.filter(id=int(job_id))
        job.delete()
        messages.success(request,f'Deleted job successfully')
        return redirect('newco-posted')
    
def apply(request:HttpRequest,job_id=None):
    if request.method == 'GET':
        if job_id:
            jobs = Job.objects.get(id=int(job_id))
            jobs.applied.add(request.user)
            messages.success(request,f'Applied for the job')
        
        jobs = Job.objects.filter(applied=request.user)
        if jobs.count() == 0:
            jobs=None    
        else:
            jobs = reversed(jobs)
    # return redirect('newco-applied')
    return render(request,'newco/postedjobs.html',{'jobs': jobs} )

def unapply(request,job_id):
    if job_id:
        jobs = Job.objects.get(id=int(job_id))
        jobs.applied.remove(request.user)
        jobs = Job.objects.filter(applied=request.user)
        messages.success(request,f'Unapplied from the job successfully')
        if jobs.count() == 0:
            jobs=None    
        else:
            jobs = reversed(jobs)
        
    return redirect('newco-applied')


def job_profile(request,job_id):
    job = Job.objects.get(id=job_id)
    applied = job.applied.all()
    if applied.count() == 0:
        applied = None

    return render(request,'newco/jobprofile.html',{
        'job':job,
        'applied':applied
    })

@login_required
def profile(request,uname):
    try:
        user = User.objects.get(username=uname)
        user_dict = model_to_dict(user)
        u1 = UserProfile.objects.get(user=request.user)
        u1_dict = model_to_dict(u1)
        user_dict.update(u1_dict)
        return render(request, 'newco/profile.html', {'loggeduser': user_dict})
    except User.DoesNotExist:
        return HttpResponse(f'Error: User {uname} does not exist')