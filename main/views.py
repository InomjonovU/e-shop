from django.shortcuts import render, redirect, get_object_or_404
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
def products(request):
    return render(request, 'products.html', {'products': Product.objects.all(), 'categories': Category.objects.all()})

@login_required(login_url='login')
def settings(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = User.objects.get(id=request.user.id)
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('index')

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
def base(request):
    return render(request, 'base.html', {'user': request.user})

@login_required(login_url='login')
def enter(request):
    context = {'enters': Enter.objects.all(), 'categories': Category.objects.all()}
    return render(request, 'enter.html', context=context)

@login_required(login_url='login')
def enter_item(request, enter_id):
    enter = Enter.objects.get(id=enter_id)
    enter_items = EnterItem.objects.filter(enter=enter)
    total_price = 0
    for item in enter_items:
        total_price += item.product.price * item.quantity
    context = {'items': enter_items, 'products': Product.objects.all(), 'enter': enter, 'total_price': total_price}
    return render(request, 'enter_item.html', context=context)

@login_required(login_url='login')
def edit_enter_item(request, enter_item_id):
    enter_item = get_object_or_404(EnterItem, id=enter_item_id)
    products = Product.objects.all()

    if request.method == 'POST':
        enter_item.product = Product.objects.get(id=request.POST['product'])
        enter_item.quantity = int(request.POST['quantity'])
        enter_item.save()
        return redirect('enter_item', enter_id=enter_item.enter.id)

    return render(request, 'edit_enter_items.html', {'enter_item': enter_item, 'products': products})

@login_required(login_url='login')
def filter_enter(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        enters = Enter.objects.all()
        if search:
            enters = enters.filter(description__icontains=search)
        if start_date:
            enters = enters.filter(created_at__gte=start_date)
        if end_date:
            enters = enters.filter(created_at__lte=end_date)

        return render(request, 'enter.html', {'enters': enters})
    return redirect('enter')

@login_required(login_url='login')
def filter_enter_item(request, enter_id):
    if request.method == 'GET':
        search = request.GET.get('search')

        if search:
            enter = Enter.objects.get(id=enter_id)
            enter_items = EnterItem.objects.filter(enter=enter, product__name__icontains=search)
            return render(request, 'enter_item.html', {'items': enter_items, 'enter': enter})

    return redirect('enter_item', enter_id=enter_id)

@login_required(login_url='login')
def out(request):
    context = {'outs': Out.objects.all(), 'categories': Category.objects.all()}
    return render(request, 'out.html', context=context)

@login_required(login_url='login')
def out_item(request, out_id):
    out = Out.objects.get(id=out_id)
    out_items = OutItem.objects.filter(out=out)
    total_price = 0
    for item in out_items:
        total_price += item.product.price * item.quantity
    context = {'items': out_items, 'products': Product.objects.all(), 'out': out, 'total_price': total_price}
    return render(request, 'out_item.html', context=context)

@login_required(login_url='login')
def filter_out(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        outs = Out.objects.all()
        if search:
            outs = outs.filter(description__icontains=search)
        if start_date:
            outs = outs.filter(created_at__gte=start_date)
        if end_date:
            outs = outs.filter(created_at__lte=end_date)

        return render(request, 'out.html', {'outs': outs})
    return redirect('out')

@login_required(login_url='login')
def filter_out_item(request, out_id):
    if request.method == 'GET':
        search = request.GET.get('search')

        if search:
            out = Out.objects.get(id=out_id)
            out_items = OutItem.objects.filter(out=out, product__name__icontains=search)
            return render(request, 'out_item.html', {'items': out_items, 'out': out})

    return redirect('out_item', out_id=out_id)

@login_required(login_url='login')
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    enters = EnterItem.objects.filter(product=product)
    outs = OutItem.objects.filter(product=product)
    return render(request, 'product_detail.html', {'product': product, 'enters': enters, 'outs': outs})

@login_required(login_url='login')
def add_enter(request):
    context = {
        'products': Product.objects.all(),
    }
    if request.method == 'POST':
        description = request.POST['description']
        enter = Enter.objects.create(description=description)
        enter_items = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        for product_id, quantity in zip(enter_items, quantities):
            EnterItem.objects.create(enter=enter, product=Product.objects.get(id=product_id), quantity=int(quantity))
        return redirect('enter_item', enter_id=enter.id)
    return render(request, 'add_enter.html', context=context)

@login_required(login_url='login')
def edit_enter(request, enter_id):
    enter = get_object_or_404(Enter, id=enter_id)
    enter_items = EnterItem.objects.filter(enter=enter)
    products = Product.objects.all()

    if request.method == 'POST':
        enter.description = request.POST['description']
        enter.save()

        for item in enter_items:
            item.delete()

        enter_items = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        for product_id, quantity in zip(enter_items, quantities):
            EnterItem.objects.create(enter=enter, product=Product.objects.get(id=product_id), quantity=int(quantity))

        return redirect('enter_item', enter_id=enter.id)

    return render(request, 'edit_enter.html', {'enter': enter, 'items': enter_items, 'products': products})

@login_required(login_url='login')
def add_out(request):
    context = {'products': Product.objects.all()}
    if request.method == 'POST':
        out = Out.objects.create(description=request.POST['description'])
        out_items = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        for product_id, quantity in zip(out_items, quantities):
            OutItem.objects.create(out=out, product=Product.objects.get(id=product_id), quantity=int(quantity))
        return redirect('out_item', out_id=out.id)
    return render(request, 'add_out.html', context=context)

@login_required(login_url='login')
def edit_out(request, out_id):
    out = get_object_or_404(Out, id=out_id)
    out_items = OutItem.objects.filter(out=out)
    products = Product.objects.all()

    if request.method == 'POST':
        out.description = request.POST['description']
        out.save()

        for item in out_items:
            item.delete()

        out_items = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        for product_id, quantity in zip(out_items, quantities):
            OutItem.objects.create(out=out, product=Product.objects.get(id=product_id), quantity=int(quantity))

        return redirect('out_item', out_id=out.id)
    return render(request, 'edit_out.html', {'out': out, 'items': out_items, 'products': products})

@login_required(login_url='login')
def customers(request):
    return render(request, 'customers.html')