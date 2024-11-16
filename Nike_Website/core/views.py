from django.shortcuts import render,redirect,get_object_or_404
from . forms import RegistrationForm,AuthenticateForm,UserProfileForm,AdminProfileForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from . models import Shoes,Shoes_cart
# Create your views here.


def index(request):
    return render(request, 'core/index.html')
# =======================================================================================



def registration(request):
    if request.method == 'POST':
            regf = RegistrationForm(request.POST)
            if regf.is_valid():
                regf.save()
                messages.success(request,'Registration Successfull !!')
                return redirect('registration')    
    else:
        regf  = RegistrationForm()
    return render(request,'core/register.html',{'regf':regf})

def log_in(request):
    if not request.user.is_authenticated:  # check whether user is not login ,if so it will show login option
        if request.method == 'POST':       # otherwise it will redirect to the profile page 
            mf = AuthenticateForm(request,request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            mf = AuthenticateForm()
        return render(request,'core/login.html',{'mf':mf})
    else:
        return redirect('profile')

def profile(request):
    if request.user.is_authenticated:  # This check wheter user is login, if not it will redirect to login page
        if request.method == 'POST':
            if request.user.is_superuser == True:
                mf = AdminProfileForm(request.POST,instance=request.user)
            else:
                mf = UserProfileForm(request.POST,instance=request.user)
            if mf.is_valid():
                mf.save()
                messages.success(request,'Profile Updated Successfully !!')
        else:
            if request.user.is_superuser == True:
                mf = AdminProfileForm(instance=request.user)
            else:
                mf = UserProfileForm(instance=request.user)
        return render(request,'core/profile.html',{'name':request.user,'mf':mf})
    else:                                                # request.user returns the username
        return redirect('login')

def log_out(request):
    logout(request)
    return redirect('index')


def changepassword(request):                                       # Password Change Form               
    if request.user.is_authenticated:                              # Include old password 
        if request.method == 'POST':                               
            cpf =PasswordChangeForm(request.user,request.POST)
            if cpf.is_valid():
                cpf.save()
                update_session_auth_hash(request,cpf.user)
                return redirect('profile')
        else:
            cpf = PasswordChangeForm(request.user)
            return render(request,'core/changepassword.html',{'cpf':cpf})
    else:
        return redirect('login')
    

def sneakers(request):
    cs = Shoes.objects.filter(category='SNEAKERS')
    return render(request,'core/sneakers.html',{'cs':cs})


def football_shoes(request):
    fs = Shoes.objects.filter(category='FOOTBALL SHOES')
    return render(request,'core/football_shoes.html',{'fs':fs})

def running_shoes(request):
    rs = Shoes.objects.filter(category='RUNNING SHOES')
    return render(request,'core/running_shoes.html',{'rs':rs})

def card_info(request,id):
    fs = Shoes.objects.get(pk=id)
    return render(request,'core/card_info.html',{'fs':fs})


def add_to_cart(request,id):
   fs = Shoes.objects.get(pk=id)
   user=request.user
   Shoes_cart  (user=user,product=fs).save()
   messages.success(request,"Added to cart successfully")
   return redirect('card_info',id)


def show_cart(request):
    fs= Shoes_cart.objects.filter(user=request.user)
    return render(request,'core/show_cart.html',{'fs':fs})


def add_quantity(request,id):
    if request.user.is_authenticated:
        product = get_object_or_404(Shoes_cart,pk=id)
        product.quantity+=1
        product.save()
        return redirect('viewcart')
    else:
        return redirect('login')

def delete_quantity(request,id):
    if request.user.is_authenticated:
        product = get_object_or_404(Shoes_cart,pk=id)
        if product.quantity>1:
            product.quantity-=1
            product.save()
        return redirect('viewcart')
    else:
        return redirect('login')
    
def delete_cart(request,id):
    pet_cart =Shoes_cart.objects.get(pk=id)
    pet_cart.delete()
    return redirect('viewcart')