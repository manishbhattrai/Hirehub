from django.db import models
from django.contrib.auth.models import AbstractUser

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
