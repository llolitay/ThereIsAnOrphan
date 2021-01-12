from django.contrib import admin
from django.urls import path,include

import Manager.views as views
urlpatterns = [
    # path('index/',views.index,name = 'employee_index'),
    # path('edit_children/',views.edit_children,name = 'employee_edit_children'),
    # path('update_child/',views.update_child,name = 'employee_update_child'),
    #
    # path('edit_my_info/',views.edit_my_info,name='employee_edit_my_info'),
    # path('update_my_info/',views.update_my_info,name='employee_update_my_info'),
    #
    # path('todo_list/',views.ToDo_List,name='employee_ToDo_List'),
    # path('update_todo_list',views.update_todo_list,name='employ_update_todo_list'),
    # path('update_todo_list_read',views.todo_list_read,name='employ_update_todo_list_read'),
    # path('delete_update_todo_list',views.delete_todo_list,name='employ_delete_todo_list'),
    # path('completed_todo_list',views.complete_todo_list,name='employ_complete_todo_list'),
    #
    # path('audit/',views.Audit,name='employee_audit'),
    # path('alter_audit',views.add_audit,name='employee_edit_audit'),


    path('index/',views.index,name='manager_index'),
    path('edit_all_children',views.edit_children,name='manager_edit_all_children'),
    path('update_child',views.update_child,name='manager_update_child'),

    path('edit_stuff',views.edit_stuff,name='manager_edit_stuff'),
    path('update_stuff',views.update_stuff,name='manager_update_stuff'),

    path('edit_my_info',views.edit_my_info,name='manager_edit_my'),
    path('update_my_info',views.update_my_info,name='manager_update_my'),

    path('todo_list/',views.ToDo_List,name='manager_ToDo_List'),
    path('update_todo_list', views.update_todo_list, name='manager_update_todo_list'),
    # path('update_todo_list_read', views.todo_list_read, name='manager_update_todo_list_read'),
    # path('delete_update_todo_list', views.delete_todo_list, name='manager_delete_todo_list'),
    # path('completed_todo_list', views.complete_todo_list, name='manager_complete_todo_list'),
    path('audit/',views.Audit,name='manager_edit_audit')
]