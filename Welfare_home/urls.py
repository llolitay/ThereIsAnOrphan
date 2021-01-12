"""Welfare_home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path,include
from App import views
import Employee.urls as Employee_urls
import Manager.urls as Manager_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('register/',views.register,name = 'register'),
    path('CheckID/',views.CheckID,name = 'CheckID'),
    path('logout/',views.logout,name='logout'),

    path('employee/',include((Employee_urls,'Employee'),namespace='Employee')),
    path('manager/',include((Manager_urls,'Manager'),namespace='Manager')),
]
