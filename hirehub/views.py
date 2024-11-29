from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CustomRegistrationForm,CustomAuthenticationForm
from django.contrib.auth import login,authenticate,logout

# Create your views here.

def home(request):
    return render(request,'home.html')

def user_create(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)

        ##print(request.POST)


        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomRegistrationForm()
    
    context ={
        'form':form
    }
    return render(request,'signup.html', context)


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)

        ##print(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            ##print(f"Email: {email}, Password: {password}")

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
    
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form':form
    }

    return render(request, 'login.html', context)

def user_logout(user,request):
    logout(request,user)