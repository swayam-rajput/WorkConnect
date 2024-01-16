from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

handler404 = 'newco.views.custom_404'

urlpatterns = [
    path('login',views.log_in,name='newco-login'),
    path('logout',views.log_out,name='newco-logout'),
    path('register',views.register,name='newco-register'),
    path('home',views.homepage,name='newco-home'),
    path('',views.homepage,name='newco-home'),
    path('addjob',views.addjob,name='newco-add-job'),
    path('profile/<str:uname>',views.profile,name='newco-profile'),
    path('posts',views.posts,name='newco-posted'),
    path('listings',views.listings,name='newco-listings'),
    path('listings/<str:filterby>',views.listings,name='newco-listings'),
    path('delete/<int:job_id>',views.delete_job,name='newco-delete'),
    path('post/apply/<int:job_id>',views.apply,name='newco-apply'),
    path('post/<int:job_id>',views.job_profile,name='newco-job-profile'),
    path('post/unapply/<int:job_id>',views.unapply,name='newco-unapply'),
    path('post/applied/',views.apply,name='newco-applied')
]
