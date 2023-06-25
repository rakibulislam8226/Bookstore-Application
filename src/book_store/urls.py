from django.urls import path
from .views import *


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store/', store , name='store'),

    #Authentication
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
]
