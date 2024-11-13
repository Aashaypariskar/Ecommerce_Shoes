from django.contrib import admin
from . models import Shoes

@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'small_description','description','original_price','discounted_price')