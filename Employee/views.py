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
            'pn': pn,
            'edit_children':'active',
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
    return HttpResponse(res['result'])

def edit_my_info(request):

    if request.method == 'GET':
        print(request.user.username)
        name = models.Employee.objects.get(num=request.user.username).name
        position = models.Employee.objects.get(num=request.user.username).position
        user = models.Employee.objects.get(num=request.user.username)

        ToDoList_new = 0
        context = {
            'name':name,
            'position':position,
            'ToDoList_new': ToDoList_new,
            'user':user,
            'Edit': 'active',
            'edit_my':'active',
        }
        return render(request,'Employee/edit_my_info.html',context)

def update_my_info(request):
    str = request.GET.get("str", None)
    num = request.GET.get("num",None)
    name = request.GET.get("name",None)
    ethnic_group = request.GET.get('ethnic_group',None)
    gender = request.GET.get('gender',None)
    password = request.GET.get('password',None)
    confirmed_password = request.GET.get('confirmed_password',None)
    edu = request.GET.get('edu',None)
    age = request.GET.get('age',None)
    position = request.GET.get('position',None)
    tele = request.GET.get('tele',None)
    address = request.GET.get('address',None)

    print(password,confirmed_password,age,tele,address)

    if password == '':
        return HttpResponse('password_error')
    if confirmed_password == '':
        return HttpResponse('confirmed_password_error')
    if age == '':
        return HttpResponse('age_error')
    if tele == '':
        return HttpResponse('tele_error')
    if address == '':
        return HttpResponse('address_error')
    if password != confirmed_password:
        return HttpResponse('password_dont_match')

    if str == '':
        str = '无'
    res = User.objects.filter(username=num).update(password=make_password(password))
    res = models.Employee.objects.filter(num=num).update(password=password,age=age,tele=tele,address=address,brief_introduction=str)

    auth.logout(request)
    return HttpResponse('ok')