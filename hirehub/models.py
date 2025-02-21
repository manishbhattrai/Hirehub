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


class Skill(models.Model):

    SKILL_CHOICES = [
    ('mechanic','Mechanic'),
    ('carpenter','Carpenter'),
    ('plumber','Plumber'),
    ('painter','Painter'),
    ('housekeeper','House Kepper'),
    ('builder','Builder'),
    ('welders','Welders'),
    ('window-installer','Window Installer'),
    ('tile-setter', 'Tile Setter'),
    ('gardening-experts', 'Gardening Experts'),
    ('cleaner','Cleaner'),
    ('babysitter','Babysitter'),
    ('caterer','Caterer'),
    ('driver','Driver'),
    ('others','Others')
    ]

    name = models.CharField(choices=SKILL_CHOICES, max_length=50)

    def __str__(self):
        return self.name


    

User = get_user_model()
class UserProfile(models.Model):


    def validate_image(image):
        ext = os.path.splitext(image.name)[1].lower()

        if ext not in ['.jpeg','.jpg']:
            raise ValidationError("Photo Should be in .jpg or .jpeg format.")
    
    choices = [
        ('M','Male'),
        ('F','Female')
    ]
            


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    image = models.ImageField(
        null=True,blank=True,
        upload_to='media/', 
        validators=[validate_image]
        )
    
    firstname = models.CharField(max_length=50, null=False)
    middlename = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(choices=choices, max_length=5, null=False, blank=False, default='M')
    address = models.CharField(max_length=60, null=False)
    email = models.EmailField(null=False)
    description = models.TextField(max_length=200, null=True)
    facebook = models.URLField(null=True,blank=True)
    number = models.CharField(
        max_length=15,null=False, 
        help_text="Enter phone number in the format: +9779XXXXXXXX or 9XXXXXXXX.")
    skills = models.ManyToManyField(Skill)
    has_profile = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile ({self.user.role})" 