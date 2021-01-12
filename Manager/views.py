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
import  math

def index(request):
    kids = models.Child.objects.filter(employee__num=request.user.username)
    name = models.Employee.objects.get(num=request.user.username).name
    position = models.Employee.objects.get(num=request.user.username).position
    stuff = models.Employee.objects.all()
    print(stuff)
    res = []
    for kid in kids:
        res.append(kid)

    user = request.user.username
    todo_list = models.To_doList.objects.filter(employee__num=user, Is_read=False)
    ToDoList_new = models.To_doList.objects.filter(employee__num=user, Is_read=False).count()
    Audit_new = models.Step_parent.objects.filter(sender__num=user, is_send=False).count()
    Audit = models.Step_parent.objects.filter(sender__num=user, is_send=False)
    context = {
        'res': res,
        'ToDoList_new': ToDoList_new,
        'name': name,
        'position': position,
        'Index': 'active',
        'ToDoList': todo_list,
        'Audit_new': Audit_new,
        'Audit': Audit,
        'stuff':stuff,
    }
    return render(request, 'Manager/manager_index.html', context)

def edit_children(request):

    if request.method =='GET':
        kids = models.Child.objects.all()
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

        ToDoList_new = models.To_doList.objects.filter(employee__num=request.user.username,Is_read=False).count()
        Audit_new = models.Step_parent.objects.filter(sender__num=request.user.username, is_send=False).count()
        context = {
            'res': res,
            'ToDoList_new': ToDoList_new,
            'Audit_new':Audit_new,
            'name': name,
            'position': position,
            'Edit':'active',
            'num_pages': num_pages,
            'numbers': numbers,
            'pn': pn,
            'edit_all_children':'active',
        }

        return render(request, 'Manager/edit_children.html', context)

def update_child(request):
    height = request.GET.get("height", None)
    weight = request.GET.get("weight", None)
    right_sight = request.GET.get("right_sight", None)
    left_sight = request.GET.get("left_sight", None)
    temperature = request.GET.get("temperature", None)
    num = request.GET.get('num', None)
    edu = request.GET.get('edu',None)
    age = request.GET.get('age',None)
    enter_time = request.GET.get('enter_time',None)
    name = request.GET.get('name',None)
    gender = request.GET.get('gender',None)
    Is_adopted = request.GET.get('Is_adopted',None)

    print(enter_time)
    print(Is_adopted)
    res = {}
    if Is_adopted is None or gender is None or height is None or weight is None or right_sight is None or left_sight is None or temperature is None or edu is None or age is None or enter_time is None or name is None:
        res['result'] = 'error'
    elif Is_adopted is "" or  gender is "" or height is "" or weight is "" or right_sight is "" or left_sight is "" or temperature is "" or edu is "" or age is "" or enter_time is "" or name is "":
        res['result'] = 'error'
    elif Is_adopted !='y' and Is_adopted != 'n':
        res['result'] = 'error'
    else:
        try:
            if Is_adopted == 'y':
                ress = models.Child.objects.filter(num=num).update(Is_adopted=True,gender=gender,height=height, weight=weight, right_sight=right_sight,
                                                    left_sight=left_sight, temperature=temperature,edu=edu,age=age,enter_time=enter_time,name=name)
            else:
                ress = models.Child.objects.filter(num=num).update(Is_adopted=False, gender=gender, height=height,
                                                                   weight=weight, right_sight=right_sight,
                                                                   left_sight=left_sight, temperature=temperature,
                                                                   edu=edu, age=age, enter_time=enter_time, name=name)

            res['result'] = 'ok'
        except:
            res['result'] = 'error'
            print('x')
    return HttpResponse(res['result'])

def edit_stuff(request):
    employee = models.Employee.objects.all()
    name = models.Employee.objects.get(num=request.user.username).name
    position = models.Employee.objects.get(num=request.user.username).position

    ToDoList_new = models.To_doList.objects.filter(employee__num=request.user.username, Is_read=False).count()
    Audit_new = models.Step_parent.objects.filter(sender__num=request.user.username, is_send=False).count()

    res = []
    for item in employee:
        if item.num != request.user.username:
            res.append(item)
    context = {
        'res': res,
        'ToDoList_new': ToDoList_new,
        'Audit_new': Audit_new,
        'name': name,
        'position': position,
        'Edit': 'active',
        'edit_stuff': 'active',
    }
    return render(request,'Manager/edit_stuff.html',context)


def update_stuff(request):
    num = request.GET.get("num", None)
    password = request.GET.get("password", None)
    name = request.GET.get('name', None)
    gender = request.GET.get("gender", None)
    age = request.GET.get('age', None)
    ethnic_groups = request.GET.get("ethnic_groups", None)
    edu = request.GET.get('edu', None)
    address = request.GET.get("address", None)
    tele = request.GET.get('tele', None)
    position = request.GET.get('position', None)
    Is_manage = request.GET.get('Is_manage',None)

    print(password,name,gender,age,ethnic_groups,edu,address,tele,position)
    print(Is_manage)
    res = {}
    if password is None or name is None or gender is None or age is None or ethnic_groups is None or address is None or edu is None or tele is None or position is None:
        res['result'] = 'error'
    elif password is "" or name is "" or gender is "" or age is "" or ethnic_groups is "" or edu is "" or address is ""  or tele is "" or position is "":
        res['result'] = 'error'
    elif Is_manage != 'y' and Is_manage != 'n':
        res['result'] = 'error'
    else:
        try:
            if Is_manage == 'y':
                ress = models.Employee.objects.filter(num=num).update(Is_manage=True,password=password, name=name, gender=gender,
                                                                   age=age, ethnic_groups=ethnic_groups, edu=edu,
                                                                    address=address, tele=tele, position=position)
                ress = User.objects.filter(username=name).update(is_superuser=True)
            else:
                ress = models.Employee.objects.filter(num=num).update(Is_manage=False,password=password, name=name, gender=gender,
                                                                   age=age, ethnic_groups=ethnic_groups, edu=edu,
                                                                    address=address, tele=tele, position=position)
                ress = User.objects.filter(username=name).update(is_superuser=False)

                res['result'] = 'ok'
        except:
            res['result'] = 'error'
    return HttpResponse(res['result'])

def edit_my_info(request):
    if request.method == 'GET':
        print(request.user.username)
        name = models.Employee.objects.get(num=request.user.username).name
        position = models.Employee.objects.get(num=request.user.username).position
        user = models.Employee.objects.get(num=request.user.username)

        ToDoList_new = models.To_doList.objects.filter(employee__num=request.user.username,Is_read=False).count()
        Audit_new = models.Step_parent.objects.filter(sender__num=user, is_send=False).count()
        context = {
            'name':name,
            'position':position,
            'ToDoList_new': ToDoList_new,
            'Audit_new':Audit_new,
            'user':user,
            'Edit': 'active',
            'edit_my':'active',
        }
        return render(request,'Manager/edit_my_info.html',context)

def update_my_info(request):
    str = request.GET.get("str", None)
    num = request.GET.get("num", None)
    name = request.GET.get("name", None)
    ethnic_group = request.GET.get('ethnic_group', None)
    gender = request.GET.get('gender', None)
    password = request.GET.get('password', None)
    confirmed_password = request.GET.get('confirmed_password', None)
    edu = request.GET.get('edu', None)
    age = request.GET.get('age', None)
    position = request.GET.get('position', None)
    tele = request.GET.get('tele', None)
    address = request.GET.get('address', None)
    str_origin = request.GET.get('str_origin', None)

    print(password, confirmed_password, age, tele, address)

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

    if name == '':
        return HttpResponse('name_error')
    if ethnic_group == '':
        return HttpResponse('ethnic_groups_error')
    if gender == '':
        return  HttpResponse('gender_error')
    if edu == '':
        return HttpResponse('edu_error')
    if position == '':
        return HttpResponse('position_error')

    if str == '':
        str = '无'
    res = User.objects.filter(username=num).update(password=make_password(password))
    res = models.Employee.objects.filter(num=num).update(password=password, age=age, tele=tele, address=address,
                                                         brief_introduction=str_origin,name=name,ethnic_groups=ethnic_group,gender=gender,
                                                         edu=edu,position=position)

    auth.logout(request)
    return HttpResponse('ok')


def ToDo_List(request):
    name = models.Employee.objects.get(num=request.user.username).name
    position = models.Employee.objects.get(num=request.user.username).position
    num = request.user.username
    ToDoList_new = models.To_doList.objects.filter(employee__num=request.user.username,Is_read=False).count()
    Audit_new = models.Step_parent.objects.filter(sender__num=request.user.username, is_send=False).count()
    todoList = models.To_doList.objects.filter(employee__num=request.user.username)
    for item in todoList:
        print(item)

    ids = []

    length = len(todoList)

    res = []
    count = 0
    temp = {}
    temp_2 = []
    for i in range(len(todoList)):
        if count == 3:
            res.append(temp_2)
            temp_2 = []
            count = 0
        print(todoList[i])
        publisher_name = models.Employee.objects.filter(num=todoList[i].publisher.num).values('name')[0]['name']
        temp.update({'publish_time':todoList[i].Publish_time})
        temp.update({'publisher_name':publisher_name})
        temp.update({'topic':todoList[i].topic})
        temp.update({'content':todoList[i].content})
        temp.update({'read':todoList[i].Is_read})
        temp.update({'id':todoList[i].id})
        temp.update({'is_complete':todoList[i].Is_completed})
        ids.append(id)
        temp_2.append(temp)
        temp = {}
        count += 1
    if len(temp_2) != 0:
        res.append(temp_2)
    context = {
        'ToDo_List':'active',
        'name':name,
        'position':position,
        'ToDoList_new':ToDoList_new,
        'Audit_new':Audit_new,
        'user':num,
        'res':res,
    }
    print(res)
    return render(request,'Manager/ToDo_List.html',context)

def update_todo_list(request):
    employee_id = request.GET.get("employee_id", None)
    publisher_id = request.GET.get("publisher_id", None)
    topic = request.GET.get("topic", None)
    content = request.GET.get('content', None)

    print(employee_id, publisher_id, topic, content)
    try:
        employee = models.Employee.objects.get(num=employee_id)
    except:
        return HttpResponse('employee_id_error')
    if employee_id == '':
        return HttpResponse('employee_id_error')
    elif publisher_id == '':
        return HttpResponse('publisher_id_error')
    elif topic == '':
        return HttpResponse('topic_error')
    elif content == '':
        return HttpResponse('content_error')

    employee = models.Employee.objects.get(num=employee_id)
    publisher = models.Employee.objects.get(num=publisher_id)
    info = {
        'publisher': publisher,
        'employee': employee,
        'content': content,
        'topic': topic,
    }

    s = models.To_doList.objects.create(**info)
    return HttpResponse('ok')

def Audit(request):
    name = models.Employee.objects.get(num=request.user.username).name
    position = models.Employee.objects.get(num=request.user.username).position
    num = request.user.username
    ToDoList_new = models.To_doList.objects.filter(employee__num=request.user.username, Is_read=False).count()
    Audit_new = models.Step_parent.objects.filter(sender__num=request.user.username, is_send=False).count()

    Audits = models.Audit.objects.filter(manager__num=num)

    step_parents = []
    for item in Audits:
        step_parents.append(item.content)
    print(step_parents)
    context = {
        'Audit':'active',
        'name':name,
        'position':position,
        'ToDoList_new':ToDoList_new,
        'Audit_new':Audit_new,
        'parents':step_parents,
        'count':Audits.count(),
    }
    return render(request,'Manager/manager_audit.html',context)