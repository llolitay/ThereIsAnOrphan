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
    res = []
    for kid in kids:
        res.append(kid)

    user = request.user.username
    todo_list = models.To_doList.objects.filter(employee__num=user,Is_read=False)
    ToDoList_new = models.To_doList.objects.filter(employee__num=user,Is_read=False).count()
    Audit_new = models.Step_parent.objects.filter(sender__num=user,is_send=False).count()
    Audit = models.Step_parent.objects.filter(sender__num=user,is_send=False)
    context = {
        'res': res,
        'ToDoList_new': ToDoList_new,
        'name': name,
        'position': position,
        'Index': 'active',
        'ToDoList':todo_list,
        'Audit_new':Audit_new,
        'Audit':Audit
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
    str_origin = request.GET.get('str_origin',None)

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
    res = models.Employee.objects.filter(num=num).update(password=password,age=age,tele=tele,address=address,brief_introduction=str_origin)

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
    return render(request,'Employee/ToDo_List.html',context)

def update_todo_list(request):
    employee_id = request.GET.get("employee_id", None)
    publisher_id = request.GET.get("publisher_id", None)
    topic = request.GET.get("topic", None)
    content = request.GET.get('content', None)

    print(employee_id,publisher_id,topic,content)
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
        'publisher':publisher,
        'employee':employee,
        'content':content,
        'topic':topic,
    }

    s = models.To_doList.objects.create(**info)
    return HttpResponse('ok')

def todo_list_read(request):
    id = request.GET.get('id',None)

    print(id)
    res = models.To_doList.objects.filter(id=id).values('Is_read')[0]['Is_read']

    if res == True:
        res = models.To_doList.objects.filter(id=id).update(Is_read=False)
        return HttpResponse('False')
    else:
        res = models.To_doList.objects.filter(id=id).update(Is_read=True)
        return HttpResponse('True')

def delete_todo_list(request):
    id = request.GET.get('id',None)
    res = models.To_doList.objects.filter(id=id).delete()
    return HttpResponse('ok')

def complete_todo_list(request):
    id = request.GET.get('id',None)
    res = models.To_doList.objects.filter(id=id).values(('Is_completed'))[0]['Is_completed']
    if res == True:
        res = models.To_doList.objects.filter(id=id).update(Is_completed=False)
        return HttpResponse('False')
    else:
        res = models.To_doList.objects.filter(id=id).update(Is_completed=True)
        return HttpResponse('True')

def Audit(request):
    ToDoList_new = models.To_doList.objects.filter(employee__num=request.user.username,Is_read=False).count()
    Audit_new = models.Step_parent.objects.filter(sender__num=request.user.username, is_send=False).count()
    name = models.Employee.objects.get(num=request.user.username).name
    position = models.Employee.objects.get(num=request.user.username).position

    step_parents = models.Step_parent.objects.filter(sender__num=request.user.username)

    context = {
        'user':request.user.username,
        'Audit':'active',
        'name': name,
        'position': position,
        'ToDoList_new':ToDoList_new,
        'Audit_new':Audit_new,
        'res':step_parents,
    }


    return  render(request,'Employee/employee_audit.html',context)

def add_audit(request):
    employee_num = request.GET.get('employee_num',None)
    step_num = request.GET.get('step_num',None)
    manager_num = request.GET.get('manager_num',None)

    judge = User.objects.filter(username=manager_num).values('is_superuser')[0]['is_superuser']
    if judge == False:
        return HttpResponse('manage_error')

    content = models.Step_parent.objects.get(num = step_num)
    applicant = models.Employee.objects.get(num= employee_num)
    manager = models.Employee.objects.get(num=manager_num)

    info = {
        'content':content,
        'applicant':applicant,
        'manager':manager
    }

    s = models.Audit.objects.create(**info)

    res = models.Step_parent.objects.filter(num=step_num).update(is_send=True)

    return HttpResponse('ok')
