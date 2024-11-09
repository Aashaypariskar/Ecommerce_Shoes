from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('registration/',views.registration,name='registration'),
    path('login/',views.log_in,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.log_out, name="logout"),
    path('changepassword/',views.changepassword, name="changepassword"),
       
]