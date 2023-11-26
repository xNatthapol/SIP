"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import environ
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from django.urls import re_path


env = environ.Env(
    # set casting, default value
    ADMIN_PATH=(str, "admin/"),
)

admin_path = env("ADMIN_PATH")

urlpatterns = [
    path("SIP/", include("SIP.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/allauth/', include('allauth.urls')),
    path('signup/', views.signup, name='signup'),
    path(admin_path, admin.site.urls),
    re_path(r'^.*$', RedirectView.as_view(url="/SIP/", permanent=False)),
]
