"""orders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy

from app.views import registration_view, \
    main_page_view, \
    login_view, \
    catalog_view, \
    cart_view, \
    remove_from_cart_view, \
    change_item_quantity_view, \
    add_to_cart_view, \
    checkout_view, \
    order_create_view, \
    congratulations_view, \
    account_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration', registration_view, name='registration'),
    path('main', main_page_view, name='main_page'),
    path('login', login_view, name="login"),
    path('account/', account_view, name='account'),
    path('catalog/', catalog_view, name='catalog'),
    path('cart/', cart_view, name='cart'),
    path('cart/remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('cart/change_item_quantity/', change_item_quantity_view, name='change_item_quantity'),
    path('cart/add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('cart/checkout/', checkout_view, name='checkout'),
    path('cart/order/', order_create_view, name='order_create'),
    path('cart/congratulations/', congratulations_view, name='congratulations'),
]
