from django.contrib import admin

from app.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, Contact, User, CartItem, Cart

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'create_date', 'user', 'status')
    list_filter = ['create_date', 'status']
    

    search_fields = ('pk', 'user__first_name', 'user__last_name', 'user__email','status')
    # fields = ['pk','create_date','user','cat__total', 'status']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class User(admin.ModelAdmin):
    pass

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass
