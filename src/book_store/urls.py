from django.urls import path
from .views import *


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store/', store , name='store'),
]
