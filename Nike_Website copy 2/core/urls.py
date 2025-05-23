from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('registration/',views.registration,name='registration'),
    path('sneakers',views.sneakers,name='sneakers'),
    path('football_shoes',views.football_shoes,name='football_shoes'),
    path('running_shoes',views.running_shoes,name='running_shoes'),
    path('card_info/<int:id>',views.card_info,name='card_info'),
    path('trending/',views.trending,name='trending'),
    path('limited_edition/',views.limited_edition,name='limited_edition'),
    path('new_arrival/',views.new_arrival,name='new_arrival'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('show_cart/',views.show_cart,name='show_cart'),
    path('login/',views.log_in,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.log_out, name="logout"),
    path('changepassword/',views.changepassword, name="changepassword"),
    path('add_quantity/<int:id>',views.add_quantity, name="add_quantity"),
    path('delete_quantity/<int:id>',views.delete_quantity, name="delete_quantity"),
    path('delete_cart/<int:id>',views.delete_cart, name="delete_cart"),
    path('address/',views.address,name='address'),
    path('payment_address/',views.payment_address,name='payment_address'),
    path('delete_address/<int:id>',views.delete_address,name='deleteaddress'),
    path('show_address/',views.show_address,name='show_address'),
    path('payment_success/<int:selected_address_id>',views.payment_success,name='paymentsuccess'),
    path('payment_failed/',views.payment_failed,name='paymentfailed'),
    path('payment/',views.payment,name='payment'),
    path('checkout',views.checkout, name="checkout"),
    path('forgotpassword/',views.forgot_password, name="forgotpassword"),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='resetpassword'),
    path('password_reset_done/', views.password_reset_done, name='passwordresetdone'),
    path('order/',views.order,name='order'),
    path('buynow/<int:id>',views.buynow,name='buynow'),
    path('buynow_payment/<int:id>/',views.buynow_payment,name='buynowpayment'),
    path('buynow_payment_success/<int:selected_address_id>/<int:id>',views.buynow_payment_success,name='buynowpaymentsuccess'),
    path('search_result/',views.search_result,name='search_result'),

       
]

#--------- THis is will add file to media folder -----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)