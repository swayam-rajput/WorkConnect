from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path('login',views.log_in,name='newco-login'),
    path('logout',views.log_out,name='newco-logout'),
    path('register',views.register,name='newco-register'),
    path('home',views.homepage,name='newco-home'),
    path('addjob',views.addjob,name='newco-add-job'),
    path('profile/<str:username>',views.profile,name='newco-profile'),
    path('posts',views.posts,name='newco-posted'),
    # path('posts/<str:id>',views.posts,name='newco-posted'),
    path('listings',views.listings,name='newco-listings'),
    path('delete/<int:job_id>',views.delete_job,name='newco-delete')
]
