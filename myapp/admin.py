from django.contrib import admin
from .models import Shirt, Order, Review, Favorite,CartItem

@admin.register(Shirt)
class ShirtAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'small_stock', 'medium_stock', 'large_stock', 'extra_large_stock', 'description')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'date_created')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'date_posted')
    search_fields = ('user__username', 'review_text')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')