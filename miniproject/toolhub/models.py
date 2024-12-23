from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'live'),(DELETE,'delete'))
    name=models.CharField(max_length=200)
    address=models.TextField()
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='customer_profile')
    phone=models.CharField(max_length=10)
    deleted_status=models.IntegerField(choices=DELETE_CHOICES,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=(
        (LIVE,'live'),
        (DELETE,'delete')
    )
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField()
    CAT_CHOICES=(
        ('air compressor','Air Compressor'),
        ('power_tools_and_accessories','Power Tools and Accessories'),
        ('machine_tools','Machine Tools'),
        )
    category = models.CharField(max_length=100,choices=CAT_CHOICES)
    description=models.TextField()
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

   

class ShippingInfo(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
