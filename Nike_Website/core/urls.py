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
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('show_cart/',views.show_cart,name='show_cart'),

    path('login/',views.log_in,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.log_out, name="logout"),
    path('changepassword/',views.changepassword, name="changepassword")
       
]

#--------- THis is will add file to media folder -----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)