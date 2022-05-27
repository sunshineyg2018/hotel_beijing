"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

from app.views import get_img, auto_token

urlpatterns = [
    path('buerjiaadmin/', admin.site.urls),
    path('get_hotel_img/',get_img),
    path('auto/token',auto_token),
    path('v1/hotel/', include(('app.urls', 'app'), namespace='hotel')),
    path('v1/user/',include(('user.urls','user'),namespace='user')),
]
