"""ERAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve 
from Main import urls as M
from Users import views as U
from api import urls as A

handler404 = 'Main.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(M),),
    path('api/', include(A),),
    path('accounts/register/', U.register, name='register'),
    path('activate/<str:u>', U.ActivateUser, name="activate user"),
    path('accounts/', include("django.contrib.auth.urls")),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
]
