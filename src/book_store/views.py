from django.shortcuts import render

# Create your views here.
from django.shortcuts import render , redirect , HttpResponseRedirect
from .models import Book
from django.views import View


# Create your views here.
class Index(View):

    def get(self , request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

    def post(self , request):
        product = request.POST.get('product')
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