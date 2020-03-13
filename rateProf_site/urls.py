"""rateProf_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from rateProf import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/list/', views.List, name='list'),
    path('api/view/', views.View, name='view'),
    path('api/average/', views.Average, name='average'),
    path('api/register/', views.Register, name='register'),
    path('api/login/', views.Login, name='login'),
    path('api/logout/', views.Logout, name='logout'),
    path('api/rate/', views.Rate, name='rate'),
]
