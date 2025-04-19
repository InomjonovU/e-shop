from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from django.utils.dateparse import parse_date

@login_required(login_url='login')
def index(request):
    context = {'user': request.user, 'total_products': Product.objects.count(), 'total_enter': Enter.objects.count(), 'total_out': Out.objects.count()}
    return render(request, 'index.html', context=context)

@login_required(login_url='login')
def movement(request):
    return render(request, 'movement.html')

@login_required(login_url='login')
def products(request):
    return render(request, 'products.html', {'products': Product.objects.all(), 'categories': Category.objects.all()})

@login_required(login_url='login')
def settings(request):
    return render(request, 'settings.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return render(request, 'index.html', {'user': user})
    return render(request, 'login.html', {'error': 'Invalid username or password!'})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['name']
        product_price = request.POST['price']
        product_quantity = request.POST['quantity']
        product_category = request.POST['category']
        product_category = Category.objects.get(id=product_category)
        product_description = request.POST['description']
        product = Product(name=product_name, description=product_description, price=product_price, quantity=product_quantity, category=product_category)

        product.save()
        return render(request, 'add_product.html', {'categories': Category.objects.all(), 'success': True})
    return render(request, 'add_product.html', {'categories': Category.objects.all(), 'success': False})

@login_required(login_url='login')
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.category = Category.objects.get(id=request.POST['category'])
        product.description = request.POST['description']
        product.save()
        return redirect('products')
    return render(request, 'edit_product.html', {'product': product, 'categories': Category.objects.all()})
@login_required(login_url='login')
def filter_products(request):
    search = request.GET.get('search')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    products = Product.objects.all()
    if search:
        products = products.filter(name__icontains=search)
    if category:
        products = products.filter(category__id=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    return render(request, 'products.html', {'products': products, 'categories': Category.objects.all()})

@login_required(login_url='login')
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('products')

@login_required(login_url='login')
def add_movement(request):
    products = Product.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 0))
        movement_type = request.POST.get('movement_type')
        product = Product.objects.get(id=product_id)

        if movement_type == '0':
            if product.quantity < quantity:
                return render(request, 'add_movement.html', {'error': 'Maxsulot yetarli emas!', 'products': products})
            movement = Out(product=product, quantity=quantity)
        elif movement_type == '1':
            movement = Enter(product=product, quantity=quantity)
        movement.save()
        return redirect('movement')

    return render(request, 'add_movement.html', {'products': products})

@login_required(login_url='login')
def movement_filter(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        movement_type = request.GET.get('type')
        date = request.GET.get('date')
        product_id = request.GET.get('product_id')

def base(request):
    return render(request, 'base.html', {'user': request.user})