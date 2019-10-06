from django.contrib import admin

from app.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, Contact, User, CartItem, Cart, Manufacturer


# Order's admin actions

def make_order_confirm(modelAdmin, request, queryset):
    queryset.update(status='Подтвержден')


make_order_confirm.short_description = 'Пометить как подтвержденные'


def make_order_assemble(modelAdmin, request, queryset):
    queryset.update(status='Собран')


make_order_assemble.short_description = 'Пометить как собранные'


def make_order_send(modelAdmin, request, queryset):
    queryset.update(status='Отправлен')


make_order_send.short_description = 'Пометить как отправленные'


def make_order_delivered(modelAdmin, request, queryset):
    queryset.update(status='Доставлен')


make_order_delivered.short_description = 'Пометить как доставленные'


def make_order_cancled(modelAdmin, request, queryset):
    queryset.update(status='Отменен')


make_order_cancled.short_description = 'Пометить как отмененные'


# Admin models

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'create_date', 'user', 'status')
    list_filter = ('create_date', 'status')
    ordering = ('-create_date',)
    search_fields = ('pk', 'user__first_name', 'user__last_name', 'user__email','status')
    actions = [make_order_confirm, make_order_assemble, make_order_send, make_order_delivered, make_order_cancled]


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name', 'second_name')
    list_filter = ('date_joined',)
    ordering = ('-date_joined',)
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('product', 'shop', 'quantity', 'price')
    list_filter = ('shop', 'shop__name')
    search_fields = ('product__name', 'quantity', 'shop__name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'model', 'manufacturer')
    list_filter = ('category__name', 'model', 'manufacturer__name')
    search_fields = ('name', 'category__name', 'model', 'manufacturer__name')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'url')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cart_total')
    search_fields = ('id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'productinfo', 'quantity', 'item_total')
    list_filter = ('productinfo__shop__name',)
    search_fields = ('id',)


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'parameter', 'value')
    list_filter = ('product__name', 'parameter__name')
    search_fields = ('product__name', 'parameter__name')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ('name',)
