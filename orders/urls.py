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

from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/registration/', views.registration_view, name='registration'),
    path('account/login/', views.login_view, name="login"),
    path('account/profile', views.account_view, name='account'),
    path('account/order/<int:id>', views.account_order_view, name='account_order'),
    path('main/', views.main_page_view, name='main_page'),
    path('shop/catalog/', views.catalog_view, name='catalog'),
    path('shop/category/<str:slug>/', views.products_of_category_view, name='category'),
    path('shop/product/<str:slug>/', views.product_detail_view, name='product'),
    path('shop/cart/', views.cart_view, name='cart'),
    path('shop/cart/remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('shop/cart/change_item_quantity/', views.change_item_quantity_view, name='change_item_quantity'),
    path('shop/cart/change_productinfo_cart/', views.change_productinfo_view, name='change_productinfo'),
    path('shop/cart/add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('shop/cart/checkout/', views.checkout_view, name='checkout'),
    path('shop/cart/order/', views.order_create_view, name='order_create'),
    path('shop/cart/congratulations/', views.congratulations_view, name='congratulations'),
    path('api/v1/', include('api.urls')),
]

