from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from .forms import CustomRegistrationForm,CustomAuthenticationForm,SellerProfileForm,BuyerProfileForm
from django.contrib.auth import login,authenticate,logout
from .models import UserProfile, CustomUser
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


##rendering homepage with 4 list of users who has role of seller.

def home(request):
    page = UserProfile.objects.filter(user__role = 'seller').select_related('user').prefetch_related('skills')[:4]
    return render(request,'home.html',{'page':page})




##function for creating a user account

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





##function for role based user login.

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
                ##print(user_role)
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
    return redirect('home')






##logic for role based profile setup.

@login_required(login_url='login')
def profile_setup(request):

    if request.user.role not in ["seller", "buyer"]:
        return redirect('login')

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if user_profile.has_profile:
        return redirect('/')

    if request.method == 'POST':
        if request.user.role == "seller":
            form = SellerProfileForm(request.POST, request.FILES, instance=user_profile)
        else:
            form = BuyerProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            user_profile = form.save(commit=False)
            
            user_profile.save()
            form.save_m2m()

            user_profile.has_profile = True
            user_profile.save()

            return redirect('/')

    else:
        if request.user.role == "seller":
            form = SellerProfileForm(instance=user_profile)
        else:
            form = BuyerProfileForm(instance=user_profile)

    return render(request, 'user_profile_form.html', {'form': form})




@login_required(login_url='login')
def user_profile(request):
    profile = UserProfile.objects.filter(user = request.user)

    context = {
        'profile':profile
    }
    return render(request,'user_profile.html',context)






@login_required(login_url='login')
def profile_update(request,id):
    update = UserProfile.objects.get(id=id)
    if request.user.role == "seller":
        form = SellerProfileForm( instance=update)
    else:
        form = BuyerProfileForm(instance=update)
    
    if request.method == 'POST':
        if request.user.role == "seller":
            form = SellerProfileForm(request.POST, request.FILES, instance=update)
        
        else:
            form = BuyerProfileForm(request.POST, request.FILES, instance=update)
        
        if form.is_valid():
            user_profile = form.save(commit=False)
            
            user_profile.save()
            form.save_m2m()
            return redirect('profile')
    
    else:
        if request.user.role == "seller":
            form = SellerProfileForm(instance=update)
        else:
            form = BuyerProfileForm(instance=update)

    return render(request, 'update_profile.html',{'form':form})







@login_required(login_url='login')
def user_delete(request,id):

    try:
         user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        raise Http404("User doesnot exist.")
    
    user.delete()
    return redirect('login')






def aboutus(request):
    return render(request,'aboutus.html')






@login_required(login_url='login')
def profile_view(request,id):

    users = get_object_or_404(CustomUser, id=id)
    profile = users.userprofile

    context = {
        "users":users,
        "profile":profile
    }

    return render(request,'profile_view.html',context)





## creating reusable function.


def get_seller_profiles():
    return UserProfile.objects.filter(user__role = 'seller').select_related('user').prefetch_related('skills').order_by('id')



## this function shows the detail of the users.

@login_required(login_url='login')
def main_page(request):
    list = get_seller_profiles()

    paginator = Paginator(list,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj':page_obj,
    }
    return render(request,'main_page.html',context)







@login_required(login_url='login')
def search_list(request):
     
    query = request.GET.get('search', '')

    if query:
        results = UserProfile.objects.filter(address__icontains = query) | UserProfile.objects.filter(skills__name__icontains = query)
        results = results.distinct()
    
    else:
        query = UserProfile.objects.all()

    list = get_seller_profiles()

    filtered_results = results.filter(user__role = 'seller')

    paginator = Paginator(filtered_results,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
     
    context = {
        'query':query,
        'results':results,
        'list':list,
        'page_obj':page_obj,
    }
        
        
    return render(request,'search.html',context)