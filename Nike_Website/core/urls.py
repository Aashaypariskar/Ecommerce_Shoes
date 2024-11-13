from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('registration/',views.registration,name='registration'),
    path('sneakers',views.sneakers,name='sneakers'),
    path('football_shoes',views.football_shoes,name='football_shoes'),
    path('running_shoes',views.running_shoes,name='runningshoes'),


    path('login/',views.log_in,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.log_out, name="logout"),
    path('changepassword/',views.changepassword, name="changepassword")
       
]