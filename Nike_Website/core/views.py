from django.shortcuts import render,redirect
from . forms import RegistrationForm,AuthenticateForm,UserProfileForm,AdminProfileForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
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