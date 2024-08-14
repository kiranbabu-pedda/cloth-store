from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Shirt(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='shirts/')
    back_image = models.ImageField(upload_to='shirts/')
    small_stock = models.PositiveIntegerField(default=0)
    medium_stock = models.PositiveIntegerField(default=0)
    large_stock = models.PositiveIntegerField(default=0)
    extra_large_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shirt, on_delete=models.CASCADE)
    size = models.CharField(max_length=20,choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('extra_large', 'Extra Large')])
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s cart: {self.product.name} (Quantity: {self.quantity}, Size: {self.size})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shirt, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')
        
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shirt, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.product.name}"
    


class Sizes(models.Model):
    shirt = models.OneToOneField(Shirt, on_delete=models.CASCADE)
    small_stock = models.PositiveIntegerField(default=0)
    medium_stock = models.PositiveIntegerField(default=0)
    large_stock = models.PositiveIntegerField(default=0)
    extra_large_stock = models.PositiveIntegerField(default=0)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'shirt')  

    def __str__(self):
        return f"{self.user.username}'s cart: {self.shirt.name} (Quantity: {self.quantity})"
    