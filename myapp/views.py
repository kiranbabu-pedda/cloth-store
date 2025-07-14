from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import Shirt, CartItem, Order, Review, Favorite, Cart,Sizes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages

def shirts_list(request):
    shirts = Shirt.objects.all()
    cart_count = CartItem.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'myapp/shirts_list.html', {'shirts': shirts,'cart_count': cart_count})


def add_to_cart(request, shirt_id):
    if not request.user.is_authenticated:
        return redirect('login')

    shirt = get_object_or_404(Shirt, id=shirt_id)
    size = request.POST.get('size')

    if size not in ['small', 'medium', 'large', 'extra_large']:
        messages.error(request, 'Invalid size selected.')
        return redirect('shirts_list')

    
    stock_field = f'{size}_stock'
    current_stock = getattr(shirt, stock_field)

    if current_stock > 0:
        
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=shirt, size=size)
        if not created:
            if cart_item.quantity < current_stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, f"Only {current_stock} of this size is available in stock.")
        else:
            cart_item.save()
       
    else:
        messages.warning(request, 'Size not available in stock.')
    
    return redirect('shirts_list')



def buy_now(request, shirt_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    shirt = get_object_or_404(Shirt, id=shirt_id)
    size = request.POST.get('size')

    if size not in ['small', 'medium', 'large', 'extra_large']:
        messages.error(request, 'Invalid size selected.')
        return redirect('shirts_list')

    stock_field = f'{size}_stock'
    current_stock = getattr(shirt, stock_field)

    if current_stock > 0:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=shirt, size=size)
        if not created:
            if cart_item.quantity < current_stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, f"Only {current_stock} of this size is available in stock.")
        else:
            cart_item.save()
        
        
        return redirect('billing')
    else:
        messages.warning(request, 'Size not available in stock.')
    
    return redirect('shirts_list')


def logout_view(request):
    logout(request)
    return redirect('shirts_list')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shirts_list')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        login(request, user)
        return redirect('shirts_list')
    return render(request, 'myapp/register.html')

@login_required
def place_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('shirts_list')
        
        # Process order and update stock
        for item in cart_items:
            size = item.size
            stock_field = f'{size}_stock'

            current_stock = getattr(item.product, stock_field, None)
            if current_stock is None:
                messages.error(request, f"Invalid size '{size}' for product {item.product.name}.")
                return redirect('billing')
            
            if current_stock < item.quantity:
                messages.error(request, f"Not enough stock for {item.product.name} size {size}. Available: {current_stock}")
                return redirect('billing')
            
            # Create order
            Order.objects.create(user=request.user, product=item.product, quantity=item.quantity)

            # Decrease stock
            setattr(item.product, stock_field, current_stock - item.quantity)
            item.product.save()

        # Clear cart
        cart_items.delete()

        # Handle review and rating safely
        review_text = request.POST.get('review', '').strip()
        try:
            rating = int(request.POST.get('rating', 0))
        except (ValueError, TypeError):
            rating = 0

        if review_text and 1 <= rating <= 5:
            Review.objects.create(user=request.user, review_text=review_text, rating=rating)
            messages.success(request, "Thank you for your review!")

        messages.success(request, "Your order has been placed successfully!")
        return render(request, 'myapp/order_placed.html')
    
    return redirect('shirts_list')

@login_required
def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    product = cart_item.product
    size = cart_item.size

    
    if size == 'small':
        stock_field = 'small_stock'
    elif size == 'medium':
        stock_field = 'medium_stock'
    elif size == 'large':
        stock_field = 'large_stock'
    elif size == 'extra_large':
        stock_field = 'extra_large_stock'
    else:
        messages.error(request, "Invalid size.")
        return redirect('billing')

    
    current_stock = getattr(product, stock_field)

    if action == 'add':
        if cart_item.quantity < current_stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, f"Only {current_stock} of this size is available in stock.")
    
    elif action == 'remove':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            messages.error(request, "Cannot remove item as quantity is already at the minimum.")
    
    else:
        messages.error(request, "Invalid action.")
    
    return redirect('billing')


@login_required
def billing(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'myapp/billing.html', {'cart_items': cart_items, 'total': total})

def delete_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('billing')

def company_details(request):
    return render(request, 'myapp/company_details.html')


def add_favorite(request, shirt_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    shirt = get_object_or_404(Shirt, id=shirt_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=shirt)
    if not created:
        favorite.delete()  
    return redirect('shirts_list')


def favorite_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'myapp/favorites_list.html', {'favorites': favorites})

def remove_favorite(request, shirt_id):
    if not request.user.is_authenticated:
        return redirect('login')

    shirt = get_object_or_404(Shirt, id=shirt_id)
    favorite = Favorite.objects.filter(user=request.user, product=shirt).first()
    if favorite:
        favorite.delete()  
    return redirect('shirts_list')

def show_favorites(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
def shirt_detail(request, shirt_id):
    shirt = get_object_or_404(Shirt, id=shirt_id)
    return render(request, 'myapp/description.html', {'shirt': shirt})
