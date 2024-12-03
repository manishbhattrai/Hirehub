from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model



# Create your models here.



class CustomUser(AbstractUser):

    choices = [
        ('buyer','Buyer'),
        ('seller','Seller')
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(choices=choices, max_length=10, default='Buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

User = get_user_model()

class SellerProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    age = models.DateField(null=False)
    address = models.CharField(max_length=60, null=False)
    email = models.EmailField(unique=True)
    description = models.TextField(max_length=200, null=True)
    facebook = models.URLField(null=True)
    number = models.CharField(max_length=12,null=False)
    skill = models.TextField(max_length=200, null=False)
    has_profile = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"








    



