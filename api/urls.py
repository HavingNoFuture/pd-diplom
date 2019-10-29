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

from django.urls import path, include
from rest_framework import routers
from api import views


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]

router = routers.SimpleRouter()
router.register(r'partner/order', views.OrderViewSet)
router.register(r'partner/state', views.StateViewSet)
router.register(r'partner/update', views.PriceUpdateViewSet, basename='price_update')


urlpatterns += router.urls



#
#
# from django.urls import path, include
# from api import views
#
#
#
#
# urlpatterns = [
#     path('', include('djoser.urls')),
#     path('', include('djoser.urls.authtoken')),
#     path('partner/order/', views.OrderView.as_view(), name='api_order_short'),
#     path('partner/order/<int:id>', views.OrderView.as_view(), name='api_order_full'),
#     path('partner/state/', views.StateView.as_view(), name='api_state'),
#     path('partner/state/<int:id>', views.StateView.as_view(), name='api_state_post'),
#     path('partner/update/', views.PriceUpdateView.as_view(), name='api_state'),
# ]
#
