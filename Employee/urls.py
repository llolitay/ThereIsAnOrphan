from django.contrib import admin
from django.urls import path,include

import Employee.views as views

urlpatterns = [
    path('index/',views.index,name = 'employee_index'),
    path('edit_children/',views.edit_children,name = 'employee_edit_children'),
    path('update_child/',views.update_child,name = 'employee_update_child'),

    path('edit_my_info/',views.edit_my_info,name='employee_edit_my_info'),
    path('update_my_info/',views.update_my_info,name='employee_update_my_info'),

    path('todo_list/',views.ToDo_List,name='employee_ToDo_List'),
    path('update_todo_list',views.update_todo_list,name='employ_update_todo_list'),
    path('update_todo_list_read',views.todo_list_read,name='employ_update_todo_list_read'),
    path('delete_update_todo_list',views.delete_todo_list,name='employ_delete_todo_list'),
]