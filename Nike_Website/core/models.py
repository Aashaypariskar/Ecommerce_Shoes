from django.db import models
from django.contrib.auth.models import User

class Shoes(models.Model):
    
    CATEGORY_CHOICES = [
        ('SNEAKERS', 'sneakers'),
        ('FOOTBALL SHOES', 'football shoes'),
        ('RUNNING SHOES', 'running shoes'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    small_description=models.CharField(max_length=300)
    description=models.TextField()
    original_price = models.IntegerField()
    discounted_price = models.IntegerField()
    pet_image =models.ImageField(upload_to='pet_images')  # As we are using image field we have to intall 'pillow'. And we have to Define MEDIA_URL in settings.py file so that all folder should save in media directory

    def __str__(self):
        return str(self.name)
