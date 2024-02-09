from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

handler404 = 'newco.views.custom_404'

urlpatterns = [
    path('login',views.log_in,name='login'),
    path('logout',views.log_out,name='logout'),
    path('register',views.register,name='register'),
    path('home',views.homepage,name='home'),
    path('',views.homepage,name='home'),
    path('addjob',views.addjob,name='add-job'),
    path('profile/<str:uname>',views.profile,name='profile'),
    path('posts',views.posts,name='posted'),
    path('listings',views.listings,name='listings'),
    
    path('listings/<str:filterby>',views.listings,name='listings'),
    
    path('delete/<int:job_id>',views.delete_job,name='delete'),
    path('post/apply/<int:job_id>',views.apply,name='apply'),
    path('post/<int:job_id>',views.job_profile,name='job-profile'),
    path('post/',views.job_profile,name='post-info'),
    path('post/unapply/<int:job_id>',views.unapply,name='unapply'),
    path('post/applied/',views.apply,name='applied'),
    path('post/<int:job_id>/applicants',views.jobapplicants,name='applicant'),
    path('post/applicants',views.allapplicants,name='all-applicants')
]
