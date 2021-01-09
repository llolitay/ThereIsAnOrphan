from django.contrib import admin
from django.urls import path,include

import Employee.views as views

urlpatterns = [
    path('index/',views.index,name = 'employee_index'),
    path('edit_children/',views.edit_children,name = 'employee_edit_children'),
    path('update_child/',views.update_child,name = 'employee_update_child')
]