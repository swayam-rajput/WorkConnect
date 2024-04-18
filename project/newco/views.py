from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpRequest, HttpResponseNotFound
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import UserProfile,Job
import os

# Create your views here.
def custom_404(request,exception):
    return HttpResponseNotFound(request, '404.html',status=404)

def log_in(request):
    if request.method == 'POST':   
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f'User {username} logged in',extra_tags='success loggedin')
            if username == 'admin':
                return redirect('verify')
            return redirect('home')
        else:
            messages.error(request,f'Invalid credentials')
    return render(request,'newco/login.html')

def log_out(request:HttpRequest):
    """Logs out the user associated with the request object"""
    username = request.user.get_username()
    logout(request)
    messages.success(request,f'User {username} logged out',extra_tags='success loggedout')
    return redirect('login')


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
                messages.success(request, f'User {username} registered',extra_tags='success registered')
                return redirect('login')
            else:
                messages.error(request, f'Passwords do not match')
        except IntegrityError as e:
            messages.error(request, f'User {username} already exists')
            
    else:
        form = UserCreationForm()
    return render(request,'newco/register.html',{'form': form})


def homepage(request):
    jobs = Job.objects.values_list('job_specification', flat=True).distinct()
    location = Job.objects.values_list('location', flat=True).distinct()
    if request.method == 'POST':
        title = request.POST.get('jobtitle')
        loc = request.POST.get('location')
        return redirect('listings',f'title={title}&location={loc}')

    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request,'newco/home.html',{'jobs':jobs,'location':location})
    
@login_required
def listings(request: HttpRequest,filterby=None):
    jobs = Job.objects.all()
    
    title = request.POST.get('jobtitle','').strip() 
    location = request.POST.get('location','').strip()
    
    if title and location:
        jobs = jobs.filter(job_specification=title.upper(),location=location)
    elif title or location:
        if title:
            jobs = jobs.filter(job_specification=title.upper())
        if location:
            jobs = jobs.filter(location=location)
    searched = False
    if jobs.count() == 0:
        jobs = None
    else:
        searched = jobs.count()!=Job.objects.count()
    return render(request, 'newco/listings.html', {'jobs': jobs,'searched':searched})

def addjob(request:HttpRequest):
    """Creates a new job based on the information provided via the form"""
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
        return redirect('posted')
        # redirect to the jobs posted page to view the posted job and display the message there
    return render(request,'newco/addjob.html')


def posts(request):
    jobs = Job.objects.filter(user=request.user)
    if jobs.count() == 0:
        jobs = None
    else:
        jobs = reversed(jobs)
    return render(request,'newco/postedjobs.html',{'jobs':jobs})


def delete_job(request:HttpRequest,job_id):
    if request.method == 'GET':
        job = Job.objects.filter(id=int(job_id))
        job.delete()
        messages.success(request,f'Deleted job successfully')
        return redirect('posted')
    
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
    # return redirect('applied')
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
        
    return redirect('applied')


def job_profile(request,job_id):
    job = Job.objects.get(id=job_id)
    applied = job.applied.all()
    # if applied.count() == 0:
    #     applied = None
    if request.method == 'POST':
        description = request.POST.get('description')
        job_specification = request.POST.get('job_specification')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        job.description = description
        job.job_specification=job_specification
        job.salary=salary
        job.location=location
        job.save()
        messages.success(request,f'Edited post')
    return render(request,'newco/jobprofile.html',{
        'job':job,
        'applied':applied
    })
    

def profile(request:HttpRequest,uname):
    try:
        user = User.objects.get(username=uname)
        u1 = UserProfile.objects.get(user=user)
        
        if request.method == 'POST':
        
            if user.email != request.POST.get('email'):
                user.email = request.POST.get('email')
                user.save()
            u1.age = request.POST.get('age')
            u1.phno = request.POST.get('phno')
            u1.save()
            messages.success(request,f'Edited profile')
        user_dict = model_to_dict(user)
        user_in_applied_job = Job.objects.filter(applied=user).exists()
        u1_dict = model_to_dict(u1)
        user_dict.update(u1_dict)
        user_profile = get_object_or_404(UserProfile, user=user)
        return render(request, 'newco/profile.html', {'loggeduser': user_dict,'is_applied':user_in_applied_job})
    except User.DoesNotExist:
        return HttpResponse(f'Error: User {uname} does not exist')
    
def jobapplicants(request:HttpRequest,job_id):
    job = Job.objects.get(id=job_id)
    applied = job.applied.select_related('userprofile').all()
    if applied.count() == 0:
        applied = None
    return render(request,'newco/applicants.html',{'job':job,'applied':applied})

def allapplicants(request):
    jobs = Job.objects.filter(user=request.user)
    return render(request,'newco/allapplicants.html',{'jobs':jobs})

def pfp_update(request:HttpRequest):
    if request.method == 'POST':
        pfp = request.FILES.get('pfp')
        u = UserProfile.objects.get(user=request.user)
        old_profile_pic = u.profilepic
        if old_profile_pic:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, old_profile_pic.path))
            except Exception as e:
                pass
        pfp.name = request.user.username+'_pfp.jpg'
        with open(os.path.join(settings.MEDIA_ROOT, 'profile_pics', pfp.name), 'wb+') as destination:
            for chunk in pfp.chunks():
                destination.write(chunk)
        
        u.profilepic = f'profile_pics/{pfp.name}'
        u.save()
        return redirect('profile',uname=request.user)
    
def update_aadhar(request:HttpRequest,username):
    if request.method == 'POST':
        aadhar_pdf = request.FILES.get('aadharpdf')
        pdf_psd = request.POST.get('pdf_psd')
        aadhar_number = request.POST.get('aadharNumber')
        
        u = UserProfile.objects.get(user=request.user)
        old_aadhar_pdf = u.aadharpdf
        if old_aadhar_pdf:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, old_aadhar_pdf.path))
            except Exception as e:
                pass
        
        aadhar_pdf.name = f'{request.user.username}_aadhar.pdf'
        with open(os.path.join(settings.MEDIA_ROOT, 'ssn', aadhar_pdf.name), 'wb+') as destination:
            for chunk in aadhar_pdf.chunks():
                destination.write(chunk)
        
        u.aadharpdf = f'ssn/{aadhar_pdf.name}'
        u.aadhar = aadhar_number
        u.pdfpsd = pdf_psd
        u.save()
        return redirect('profile', uname=request.user)
    return render(request,'newco/update-aadhar.html',{'username':request.user.username})

def verify(request):
    if request.user.username == 'admin':
        unverified = UserProfile.objects.filter(is_verified=False).exclude(aadhar='',pdfpsd='')
        unverified = unverified.exclude(aadhar='-')
        unverified = unverified.exclude(aadharpdf="null")
        
        if unverified.count() == 0:
            unverified = None
        return render(request,'newco/admin-verif.html',{'users':unverified})
    else:
        raise Http404(request)

def verify_user(request:HttpRequest,id):
    if request.user.id == 66:
        user_profile = UserProfile.objects.get(user_id=id)
        user_profile.is_verified = True
        user_profile.save()
    return redirect('verify')

def unverify_user(request:HttpRequest,id):
    if request.user.id == 66:
        user_profile = UserProfile.objects.get(user_id=id)
        user_profile.aadhar = '-'
        user_profile.aadharpdf = None
        user_profile.pdfpsd = ''
        user_profile.save()
    return redirect('verify')
    