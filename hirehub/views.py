from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CustomRegistrationForm,CustomAuthenticationForm,SellerProfileForm,BuyerProfileForm
from django.contrib.auth import login,authenticate,logout
from .models import UserProfile
from django.contrib.auth.decorators import login_required

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

    user_role = None

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)

        ##print(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            ##print(f"Email: {email}, Password: {password}")

            user = authenticate(request, username=email, password=password)

            ##print(user)

            if user is not None:
                login(request, user)
                user_role = user.role
                print(user_role)
                return redirect('profile_setup')
                
    
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form':form,
        'user_role':user_role

    }

    return render(request, 'login.html', context)



def users_logout(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def profile_setup(request):

    if request.user.role not in ["seller","buyer"]:
        return redirect('/')
    

    user_profile,created = UserProfile.objects.get_or_create(user = request.user)
    if user_profile.has_profile:
        return redirect('/')
    
    if request.method == 'POST':
        if request.user.role == "seller":
            form = SellerProfileForm(request.POST, instance=user_profile)
        else:
            form = BuyerProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            user_profile.has_profile = True
            user_profile.save()
            return redirect('/')
    else:
        if request.user.role == "seller":
            form = SellerProfileForm(instance=user_profile)
        else:
            form = BuyerProfileForm(instance=user_profile)
    
    return render(request,'user_profile_form.html',{'form':form})

def user_profile(request):
    profile = UserProfile.objects.filter(user = request.user)

    context = {
        'profile':profile
    }
    return render(request,'user_profile',context)

    


