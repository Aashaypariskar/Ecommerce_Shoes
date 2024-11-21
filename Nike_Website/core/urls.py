from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('registration/',views.registration,name='registration'),
    path('sneakers',views.sneakers,name='sneakers'),
    path('football_shoes',views.football_shoes,name='football_shoes'),
    path('running_shoes',views.running_shoes,name='runningshoes'),
    path('card_info/<int:id>',views.card_info,name='card_info'),
    path('trending/',views.trending,name='trending'),
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
    path('delete_address/<int:id>',views.delete_address,name='deleteaddress'),
    path('show_address/',views.show_address,name='show_address'),
    # path('payment_success/<int:selected_address_id>',views.payment_success,name='paymentsuccess'),
    # path('payment_failed/',views.payment_failed,name='paymentfailed'),
    # path('payment/',views.payment,name='payment'),
    # path('order/',views.order,name='order'),

    # path('checkout/<int:id>',views.checkout, name="checkout"),

       
]

#--------- THis is will add file to media folder -----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)