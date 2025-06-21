from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request , 'home.html' ,{'products': products})


@login_required
def add_cart(request , pk):
    product = get_object_or_404(Product , id = pk)

    cart , _ = Cart.objects.get_or_create(user = request.user)
    cart_item , created  = CartItem.objects.get_or_create(cart = cart , product = product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("view_cart")

@login_required
def view_cart(request):
    cart , _ = Cart.objects.get_or_create(user = request.user)
    if request.method == "POST":
        for item in cart.items.all():
            qty = request.POST.get(f'quantity_{item.id}')
            if qty and qty.isdigit():
                item.quantity = int(qty)
                item.save()
        return redirect('view_cart')
    return render(request , 'cart.html',{'cart': cart})


@login_required
def remove_cartItem(request,pk):
    item = get_object_or_404(CartItem , id = pk , cart__user = request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart , _ = Cart.objects.get_or_create(user = request.user)
    return render (request , 'checkout.html' , {'cart': cart})


@login_required
def place_order(request):
    cart , _ = Cart.objects.get_or_create(user = request.user)
    cart_item = cart.items.all()
    if not cart_item:
        return redirect ('checkout')
    total = sum(item.product.price * item.quantity for item in cart_item)

    order = Order.objects.create(user = request.user , total = total)
    cart_item.delete()
    return render (request , 'order_put.html', {'order': order})


def category_view(request , category_name):
    products = Product.objects.filter(category__name=category_name)
    return render(request , 'category.html' , {'products': products , 'category': category_name} )