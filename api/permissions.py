from rest_framework.permissions import BasePermission


class IsShopAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='shop_admins').exists()