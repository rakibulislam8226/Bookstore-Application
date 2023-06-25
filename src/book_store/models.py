from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    

class Book(TimeStampMixin):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    publication_date = models.DateField()
    ex_price = models.DecimalField(max_digits=5, decimal_places=2, help_text='Previous price.', null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text='Present price.')

    def __str__(self):
        return self.title

    @staticmethod
    def get_book_by_id(ids):
        return Book.objects.filter (id__in=ids)
    
    @staticmethod
    def get_all_books():
        return Book.objects.all()
    

class Order(TimeStampMixin):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField (max_length=50, default='', blank=True)
    status = models.BooleanField (default=False)

    def __str__(self):
        return f'{self.book} - {self.customer}'

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-created_at')


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField (max_length=50)
    phone = models.CharField(max_length=10)
    email= models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email

    #Save the data
    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True
        return False
    
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email= email)
        except:
            return False
