from django.shortcuts import render,redirect,get_object_or_404
from . forms import RegistrationForm,AuthenticateForm,UserProfileForm,AdminProfileForm,PasswordChangeForm,CustomerForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from . models import Shoes,Shoes_cart,UserDetails,Order
# Create your views here.


def index(request):
    return render(request, 'core/index.html')
# =======================================================================================

#===============For Paypal =========================
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
#=========================================================


#================ Forgot Password ======================
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse
#=========================================================

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
    print(fs)
    return render(request,'core/card_info.html',{'fs':fs})


def trending(request):
    ts = Shoes.objects.filter(category='TRENDING')
    return render(request,'core/trending.html',{'ts':ts})



def add_to_cart(request,id):
   fs = Shoes.objects.get(pk=id)
   user=request.user
   Shoes_cart  (user=user,product=fs).save()
   messages.success(request,"Added to cart successfully")
   return redirect('card_info',id)


def show_cart(request):
    fs= Shoes_cart.objects.filter(user=request.user)
        
    return render(request,'core/show_cart.html',{'fs':fs})

# ============================== Checkout Page ==============================

def checkout(request):
    cart_items =Shoes_cart.objects.filter(user=request.user)
    total=0
    delhivery_charge=2000
    for item in cart_items:
        total+=(item.product.discounted_price*item.quantity)
        final_price =total+delhivery_charge
    address = UserDetails.objects.filter(user=request.user)
    return render(request,'core/checkout.html',{'total':total,'final_price':final_price,'address':address})



def add_quantity(request,id):
    if request.user.is_authenticated:
        product = get_object_or_404(Shoes_cart,pk=id)
        if product.quantity>=4:
            messages.error(request,"You cannot add more than 4 for this item ")
            return redirect('show_cart')
        product.quantity+=1
        product.save()
        return redirect('show_cart')
    else:
        return redirect('login')

def delete_quantity(request,id):
    if request.user.is_authenticated:
        product = get_object_or_404(Shoes_cart,pk=id)
        if product.quantity>1:
            product.quantity-=1
            product.save()
        return redirect('show_cart')
    else:
        return redirect('login')
    
def delete_cart(request,id):
    sc =Shoes_cart.objects.get(pk=id)
    sc.delete()
    return redirect('show_cart')

# ================================ Address Page =========================
def address(request):
    if request.method == 'POST':
            af =CustomerForm(request.POST)
            if af.is_valid():
                user=request.user                # user variable store the current user i.e steveroger
                name= af.cleaned_data['name']
                address= af.cleaned_data['address']
                city= af.cleaned_data['city']
                state= af.cleaned_data['state']
                pincode= af.cleaned_data['pincode']  
                UserDetails(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
                return redirect('address')           
    else:
        af = CustomerForm()
        address = UserDetails.objects.filter(user=request.user)
    return render(request,'core/address.html',{'af':af,'address':address})

def show_address(request):
    address = UserDetails.objects.filter(user=request.user)
    return render(request,'core/show_address.html',{'address':address})

def delete_address(request,id):
    if request.method == 'POST':
        de = UserDetails.objects.get(pk=id)
        de.delete()
    return redirect('show_address')


def checkout(request):

    cart_items = Shoes_cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
        final_price= delhivery_charge + total
    
    address = UserDetails.objects.filter(user=request.user)

    return render(request, 'core/checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address,})

def payment(request):

    if request.method=='POST':
        selected_address_id = request.POST.get('selected_address')

    cart_items =Shoes_cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
        final_price= delhivery_charge + total
    
    address = UserDetails.objects.filter(user=request.user)


 #============== Paypal Code =====================
   
    host = request.get_host()   # Will fecth the domain site is currently hosted on.
   
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,   #This is typically the email address associated with the PayPal account that will receive the payment.
        'amount': final_price,    #: The amount of money to be charged for the transaction. 
        'item_name': 'Pet',       # Describes the item being purchased.
        'invoice': uuid.uuid4(),  #A unique identifier for the invoice. It uses uuid.uuid4() to generate a random UUID.
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",         #The URL where PayPal will send Instant Payment Notifications (IPN) to notify the merchant about payment-related events
        'return_url': f"http://{host}{reverse('paymentsuccess',args=[selected_address_id])}",     #The URL where the customer will be redirected after a successful payment. 
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",      #The URL where the customer will be redirected if they choose to cancel the payment. 
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

 #=============== Paypal Code  End =====================

    return render(request,'core/payment.html',{'paypal':paypal_payment})

# ==================== Payment Success Page =====================================
def payment_success(request,selected_address_id):

    user= request.user
    address_data = UserDetails.objects.get(pk=selected_address_id)
    cart=Shoes_cart.objects.filter(user=request.user)
    for cart in cart:
        Order(user=user,customer=address_data,quantity=cart.quantity,pet=cart.product).save()
        cart.delete()
    return render(request,'core/payment_success.html')

# ==================== Payment Failed Page =====================================

def payment_failed(request):
    return render(request,'core/payment_failed.html')

#================================== Forget Password ====================================================

def forgot_password(request):          
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter().first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')           
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_url}',
                'fordjangopproject@gmail.com',  # Use a verified email address
                [email],
                fail_silently=False,
            )
            return redirect('passwordresetdone')
        else:
            messages.success(request,'please enter valid email address')
    return render(request, 'core/forgot_password.html')
                                         
    # return render(request,'core/forgot_password.html',)

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('passwordresetdone')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'core/reset_password.html')

def password_reset_done(request):
    return render(request, 'core/password_reset_done.html')