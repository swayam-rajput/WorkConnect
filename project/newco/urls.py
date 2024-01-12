from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path('login',views.log_in,name='newco-login'),
    path('logout',views.log_out,name='newco-logout'),
    path('register',views.register,name='newco-register'),
    path('home',views.homepage,name='newco-home'),
    # path('profile',views.profile,name='profile'),
    path('listings',views.listings,name='newco-listings')
    # path('',views.homepage,name='newco')
]
