from django.shortcuts import render,HttpResponseRedirect,reverse,HttpResponse

from django.views.generic import View,ListView
# Create your views here.
from django.contrib.auth.hashers import make_password #在注册时，将密码加密后存入
import App.models as models
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def login(request):

    if request.method == 'GET':
        UserNum = request.COOKIES.get('UserNum',"")
        Password = request.COOKIES.get('Password',"")
        rep = render(request, 'Login.html', {'num':UserNum, 'password':Password})
        rep.delete_cookie('UserNum')
        rep.delete_cookie('Password')
        rep.delete_cookie('error')
        return rep
    else:
        username = request.POST.get('num',None)
        password = request.POST.get('password',None)
        type = request.POST.get('type',None)
        user = auth.authenticate(username = username,password = password)
        if user is not None and user.is_active:
            if(type == '1' and len(models.Employee.objects.filter(num=username))!=0):
                auth.login(request,user)
                return HttpResponseRedirect(reverse('Employee:employee_index'))
            elif (type == '2' and User.objects.get(username=username).is_superuser == True):
                auth.login(request,user)
                return HttpResponseRedirect(reverse('Manager:manager_index'))
            return render(request, 'Login.html', {'num': username, 'password': password, 'type_error': 'red'})
        else:
            return render(request, 'Login.html', {'num': username, 'else_error': 'red'})

def register(request):
    if request.method == 'GET':
        return render(request,'Register.html')
    else:
        num = request.POST.get('num',None)
        password = request.POST.get('password', None)
        name = request.POST.get('name', None)
        gender = request.POST.get('gender',None)
        age = request.POST.get('age',None)
        position = request.POST.get('position',None)
        tele = request.POST.get('tele',None)
        user_info = {
            'username':num,
            'password':make_password(password),
            'is_active':1,
            'is_superuser':0,
            'is_staff':0
        }
        user = User.objects.create(**user_info)
        staff_info = {
            'num':num,
            'password':password,
            'name':name,
            'gender':gender,
            'age':age,
            'position':position,
            'tele':tele
        }
        staff = models.Employee.objects.create(**staff_info)
        rep = HttpResponseRedirect(reverse('login'))
        rep.set_cookie('UserNum',num)
        rep.set_cookie('Password',password)
        return rep
def CheckID(request):
    username = request.GET.get('username')
    message = 'ok'
    try:
        res = User.objects.get(username=username)
        message = '用户名已存在'
    except:
        pass
    return HttpResponse(message)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))