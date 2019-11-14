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

from rest_framework import routers
from rest_framework.schemas import get_schema_view

from django.urls import path, include

from api import views


state_detail = views.StateViewSet.as_view({
    'get': 'retrieve',
    'post': 'update_state_detail',
})

state_list = views.StateViewSet.as_view({
    'get': 'list',
    'post': 'update_state_list',
})

price_update = views.PriceUpdateViewSet.as_view({
    'post': 'update_price',
})

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('partner/state/<int:pk>/', state_detail, name='state-detail'),
    path('partner/state/', state_list, name='state-list'),
    path('partner/update/', price_update, name='price-update'),
    path('openapi', get_schema_view(
        title="Shop API",
        description="API for all things …",
        # version="1.0.0",
        urlconf='api.urls'
    ), name='openapi-schema'),
]

router = routers.SimpleRouter()
router.register(r'partner/order', views.OrderViewSet)

urlpatterns += router.urls
