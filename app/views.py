from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm, OrderForm, ContactForm

from app.models import Category, Product, Shop, ProductInfo, Cart, CartItem, Order


# Create your views here.
def main_page_view(request):
    return render(request, 'app/main.html')


# User's views

def registration_view(request):
    form = RegistrationForm(request.POST or None)
    context = {}
    context['form'] = form
    if form.is_valid():
        new_user = form.save(commit=False)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        new_user.set_password(password)
        new_user.first_name = form.cleaned_data['first_name']
        new_user.last_name = form.cleaned_data['last_name']
        new_user.email = email
        new_user.company = form.cleaned_data['company']
        new_user.position = form.cleaned_data['position']
        new_user.second_name = form.cleaned_data['second_name']
        new_user.save()

        login_user = authenticate(email=email, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('main_page'))
        return HttpResponseRedirect(reverse('main_page'))

    return render(request, 'app/registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    context = {}
    context['form'] = form

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        # email = User.objects.get(email=email).email

        login_user = authenticate(email=email, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('main_page'))

    return render(request, 'app/login.html', context)


# Product's views

def catalog_view(request, *args, **kwargs):
    category = request.GET.get('category')
    shop = request.GET.get('shop')

    context = {}
    context['product_infos'] = ProductInfo.objects.all()

    if category:

        context["product_infos"] = ProductInfo.objects.filter(product__category__name__iexact=category)

    if shop:
        context["product_infos"] = ProductInfo.objects.filter(shop__name__iexact=shop)

    context['shops'] = Shop.objects.all()
    context['categories'] = Category.objects.all()

    return render(request, 'app/catalog.html', context)


# Cart's views

def cart_session(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(pk=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart


def cart_view(request):
    context = {}
    context['cart'] = cart_session(request)
    return render(request, 'app/cart.html', context)


def add_to_cart_view(request):
    slug = request.GET.get('slug')
    cart = cart_session(request)
    product = ProductInfo.objects.get(product__slug=slug)
    cart.add_to_cart(product)

    cart.count_cart_total()
    return JsonResponse({})


def remove_from_cart_view(request):
    slug = request.GET.get('slug')
    cart = cart_session(request)
    product = Product.objects.get(slug=slug)
    cart.remove_from_cart(product)

    cart_total = cart.count_cart_total()
    return JsonResponse({'cart_total': cart_total})


def change_item_quantity_view(request):
    context = {}
    cart = cart_session(request)
    context['cart'] = cart
    quantity = int(request.GET.get('quantity', 1))
    item_id = int(request.GET.get('item_id', 1))

    cart_item = CartItem.objects.get(pk=item_id)
    cart_item.change_quantity(quantity)

    cart_total = cart.count_cart_total()

    return JsonResponse({'item_total': cart_item.item_total,
                         'cart_total': cart_total})


def checkout_view(request):
    context = {}
    context['cart'] = cart_session(request)
    context['categories'] = Category.objects.all()
    return render(request, 'app/checkout.html', context)


def order_create_view(request):
    context = {}
    form = OrderForm(request.POST or None)
    context['form'] = OrderForm(request.POST or None)
    cart = cart_session(request)
    context['cart'] = cart

    if form.is_valid():
        new_order = Order()
        user = request.user
        new_order.user = user
        new_order.cart = cart
        new_order.save()
        new_order.buying_type = form.cleaned_data['buying_type']
        new_order.address = form.cleaned_data['address']
        new_order.comment = form.cleaned_data['comment']
        new_order.total = cart.cart_total
        new_order.save()

        del request.session['cart_id']
        return HttpResponseRedirect(reverse('congratulations'))
    return render(request, 'app/order.html', context)


def congratulations_view(request):
    context = {}
    context['user'] = request.user
    context['categories'] = Category.objects.all()
    return render(request, 'app/congratulations.html', context)



def account_view(request):
    context = {}
    try:
        context['orders'] = Order.objects.filter(user=request.user).order_by('-pk')
    except:
        context['orders'] = None
    context['categories'] = Category.objects.all()
    context['contact_form'] = ContactForm()
    return render(request, 'app/account.html', context)
