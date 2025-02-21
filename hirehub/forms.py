from .models import CustomUser, UserProfile, Skill
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import re

class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=12, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=12, required=True, widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=CustomUser.choices, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']

        if commit:
            user.save()

        return user
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 is None:
            raise forms.ValidationError("Password is empty.")

        if password1 != password2:
            raise forms.ValidationError("Password didn't match.")
        
        if len(password1)<8:
            raise forms.ValidationError("Password must be more than 8 Characters.")
        
        return password2
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already Exists.")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']

        email_regex = r"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
        if not re.match(email_regex, email):
            raise forms.ValidationError("Enter a valid email address.")
        
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already Exists.")
        
        return email
    


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('username')

        if not email:
            raise forms.ValidationError("Email is Required.")
        
        email_regex = r"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
        if not re.match(email_regex, email):
            raise forms.ValidationError("Enter a valid email address.")
        
        try:
            user = CustomUser.objects.get(email=email)
        
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Invalid Email.")
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password is None:
            raise forms.ValidationError("Password is Required.")
        
        ##if not CustomUser.objects.filter(password=password):
          ##  raise forms.ValidationError("Password didn't match.")
        
        return password

class SellerProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = True
    )
    class Meta:
        model = UserProfile
        fields = ['image','firstname','middlename','lastname','date_of_birth','gender','address','email','description','facebook','number','skills']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        print("Email from cleaned data:", email)
       
        if not email:
            raise forms.ValidationError("Email is Required.")
        
        if email.strip() == '':
            raise forms.ValidationError("Email cannot be empty.")
        
        return email
    
    def clean_skills(self):
        skills = self.cleaned_data.get('skills')

        if not skills:
            raise forms.ValidationError("You must select atleast one skill.")
        
        if len(skills) != len(set(skills)):
            raise forms.ValidationError("Duplicate skills are not allowed.")
        
        return skills
        

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image','firstname','middlename','lastname','address']