from django.urls import path
from . import views



urlpatterns = [
    path('', views.shirts_list, name='shirts_list'),
    path('add-to-cart/<int:shirt_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:shirt_id>/', views.buy_now, name='buy_now'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('place-order/', views.place_order, name='place_order'),
    path('update-cart/<int:cart_item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('billing/', views.billing, name='billing'),
    path('delete-from-cart/<int:cart_item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('company/', views.company_details, name='company_details'),
    
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('remove_favorite/<int:shirt_id>/', views.remove_favorite, name='remove_favorite'),
    path('add_favorite/<int:shirt_id>/', views.add_favorite, name='add_favorite'),
    path('shirt/<int:shirt_id>/', views.shirt_detail, name='shirt_detail'),
]
