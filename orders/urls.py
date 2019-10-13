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
from django.conf.urls import url

from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration', views.registration_view, name='registration'),
    path('main', views.main_page_view, name='main_page'),
    path('login', views.login_view, name="login"),
    path('account/', views.account_view, name='account'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('category/<str:slug>/', views.products_of_category_view, name='category'),
    path('product/<str:slug>/', views.product_detail_view, name='product'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/change_item_quantity/', views.change_item_quantity_view, name='change_item_quantity'),
    path('cart/change_productinfo_cart/', views.change_productinfo_view, name='change_productinfo'),
    path('cart/add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/checkout/', views.checkout_view, name='checkout'),
    path('cart/order/', views.order_create_view, name='order_create'),
    path('cart/congratulations/', views.congratulations_view, name='congratulations'),
    path('api/v1/', include('api.urls')),
]

