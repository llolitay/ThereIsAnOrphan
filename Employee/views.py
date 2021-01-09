from django.shortcuts import render,HttpResponseRedirect,reverse,HttpResponse

from django.views.generic import View,ListView
# Create your views here.
from django.contrib.auth.hashers import make_password #在注册时，将密码加密后存入
import App.models as models
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import json

def index(request):
    kids = models.Child.objects.filter(employee__num=request.user.username)
    name = models.Employee.objects.get(num=request.user.username).name
    position = models.Employee.objects.get(num=request.user.username).position
    res = []
    for kid in kids:
        res.append(kid)

    ToDoList_new = 0
    context = {
        'res': res,
        'ToDoList_new': ToDoList_new,
        'name': name,
        'position': position,
        'Index': 'active'
    }
    return render(request, 'Employee/employee_index.html', context)

def edit_children(request):

    if request.method =='GET':
        kids = models.Child.objects.filter(employee__num=request.user.username)
        name = models.Employee.objects.get(num=request.user.username).name
        position = models.Employee.objects.get(num=request.user.username).position
        res = []
        pn = request.GET.get("pn", 1)
        pn = int(pn)
        for kid in kids:
            res.append(kid)


        # 分页功能
        per_page = 4
        paginator = Paginator(res, per_page)  # 1、查询结果集  2、每一页显示的记录数
        try:
            res = paginator.page(pn)  # 获取某一页记录
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            res = paginator.page(1)
        # 获取总页数
        num_pages = res.paginator.num_pages

        if num_pages >= 5:  # 总页数大于想显示的分页数字
            if pn <= 2:
                start = 1
                end = 6
            elif pn > num_pages - 2:
                start = num_pages - 4
                end = num_pages + 1
            else:
                start = pn - 2
                end = pn + 3
        else:
            start = 1
            end = num_pages + 1

        numbers = range(start, end)

        ToDoList_new = 0
        context = {
            'res': res,
            'ToDoList_new': ToDoList_new,
            'name': name,
            'position': position,
            'Edit':'active',
            'num_pages': num_pages,
            'numbers': numbers,
            'pn': pn
        }

        return render(request, 'Employee/edit_children.html', context)

def update_child(request):

    height = request.GET.get("height",None)
    weight = request.GET.get("weight",None)
    right_sight = request.GET.get("right_sight",None)
    left_sight = request.GET.get("left_sight",None)
    temperature = request.GET.get("temperature",None)
    num = request.GET.get('num',None)
    print(height, weight, right_sight, left_sight, temperature)
    res = {}
    if height is None or weight is None or right_sight is None or left_sight is None or temperature is None:
        res['result'] = 'error'
    elif height is "" or weight is "" or right_sight is "" or left_sight is "" or temperature is "":
        res['result'] = 'error'
    else:
        ress =models.Child.objects.filter(num=num).update(height=height,weight=weight,right_sight=right_sight,left_sight=left_sight,temperature=temperature)
        res['result'] = 'ok'
    return HttpResponse(json.dumps(res),content_type='application/json')