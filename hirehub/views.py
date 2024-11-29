from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CustomRegistrationForm,CustomAuthenticationForm
from django.contrib.auth import login,authenticate

# Create your views here.

def home(request):
    return HttpResponse("hello.")

def user_create(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
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
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request,username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            
    
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form':form
    }

    return render(request, 'login.html', context)