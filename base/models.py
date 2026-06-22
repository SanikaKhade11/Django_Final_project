from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    pname = models.CharField(max_length=100)
    pdesc = models.CharField(max_length=200)
    price = models.IntegerField()
    pcategory = models.CharField(max_length=100)
    trading = models.BooleanField(default=False)
    offer = models.BooleanField(default=False)
    pimage = models.ImageField(default='defaultimg.jpg', upload_to='uploads/')

    # cart  model should be user-specific and will be displayed only to me 
class Cart(models.Model):
    pname = models.CharField(max_length=100)
    price = models.IntegerField()
    pcategory = models.CharField(max_length=100)
    totalprice = models.IntegerField()
    quantity = models.IntegerField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)  #used to establish the relation between two table that is user_auth and cart                                                      #cascade is used too delete the complete record when user logged out
    

