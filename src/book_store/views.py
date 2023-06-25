from django.shortcuts import render, redirect,  HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer, CartItemSerializer
from .models import Book, Customer, Order
from .forms import BookForm
from django.views import View


# Create your views here.
class Index(View):

    def get(self , request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

    def post(self , request):
        product = request.POST.get('product')
        print('inside')
        print(product)
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('homepage')


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = Book.get_all_books()

    data = {}
    data['products'] = products

    return render(request, 'index.html', data)



class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer (first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
        error_message = self.validateCustomer (customer)

        if not error_message:
            customer.password = make_password (customer.password)
            customer.register ()
            return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 11:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'

        return error_message

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'
        return render (request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Book.get_book_by_id(ids)
        return render(request , 'cart.html' , {'products' : products} )
    

class OrderView(View):
    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Book.get_book_by_id(list(cart.keys()))

        for product in products:
            order = Order(customer_id=customer,
                          book_id=product.id,
                          price=product.price,
                          address=address,
                          quantity=cart.get(str(product.id)))
            order.save()

        request.session['cart'] = {}

        return redirect('cart')
    

@login_required
def add_book(request):
    if not request.user.is_authenticated:
        messages.error(request, 'User is not authenticated.')
        return redirect('login')

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.save()
            return redirect('homepage')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


class AddToCartAPIView(APIView):
    def post(self, request):
        book_serializer = BookSerializer(data=request.data['book'])
        cart_item_serializer = CartItemSerializer(data=request.data)

        book_serializer.is_valid(raise_exception=True)
        cart_item_serializer.is_valid(raise_exception=True)

        book = book_serializer.save()
        cart_item = cart_item_serializer.save(book=book)

        return Response(CartItemSerializer(cart_item).data, status=201)

# raw data for passing into api.
"""
{
    "book": {
        "title": "Book Title",
        "author": 1,
        "price": 9.99,
        "publication_date": "2023-06-25"
    },
    "quantity": 1
}
"""