from django.contrib import admin
from . models import Shoes,Shoes_cart,UserDetails,Order

@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'small_description','description','original_price','discounted_price']


@admin.register(Shoes_cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
    
@admin.register(UserDetails)
class CustomerAdmin(admin.ModelAdmin):
    list_display= ['id','user','name','address','city','state','pincode']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display= ['id','user','customer','pet','quantity','order_at','status',]