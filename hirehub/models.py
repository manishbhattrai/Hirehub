from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import os



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

class UserProfile(models.Model):


    phone_number_regex = RegexValidator(
      regex=r'^\+9779\d{8}$|^9\d{8}$',  
        message="Phone number must be in the format: +9779XXXXXXXX or 9XXXXXXXX."
    )

    def validate_image(image):
        ext = os.path.splitext(image.name)[1].lower()

        if ext not in ['.jpeg','.jpg']:
            raise ValidationError("Photo Should be in .jpg or .jpeg format.")
    
    choices = [
        ('M','Male'),
        ('F','Female')
    ]
            


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True,blank=True,
        upload_to='media/', 
        validators=[validate_image]
        )
    
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(choices=choices, max_length=5, null=False, blank=False, default='M')
    address = models.CharField(max_length=60, null=False)
    email = models.EmailField(unique=True,null=False)
    description = models.TextField(max_length=200, null=True)
    facebook = models.URLField(null=True,blank=True)
    number = models.CharField(
        max_length=14,null=False, 
        validators=[phone_number_regex],
        help_text="Enter phone number in the format: +9779XXXXXXXX or 9XXXXXXXX.")
    

    skill = models.TextField(max_length=200, null=False)
    has_profile = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile" 