from django.urls import path
from .middlewares.auth import auth_middleware
from .views import Cart, OrderView
from .views import *


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store/', store , name='store'),

    #Authentication
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),

    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

    path('books/add/', add_book, name='add_book'), 
    path('api/cart/add/', AddToCartAPIView.as_view(), name='add-to-cart'),
]
