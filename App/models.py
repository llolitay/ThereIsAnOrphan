from django.db import models

from datetime import datetime

#相当于在对应数据库中建表，模型修改后
#1.执行 python manage.py makemigrations
#2.执行 python manage.py migrate
# Create your models here.
class Employee(models.Model):
    num = models.CharField(verbose_name='工号', max_length=18, blank=False, unique=True, null=False, primary_key=True)
    password = models.CharField(verbose_name="密码", max_length=30, blank=False, null=False,default="000000")
    name = models.CharField(verbose_name='姓名', max_length=20, blank=False, null=False)
    gender = models.CharField(verbose_name='性别', max_length=5, blank=False, null=False)
    age = models.IntegerField(verbose_name='年龄', default=0, blank=False, null=False)
    edu = models.CharField(verbose_name='学历', default='文盲',max_length=20)
    ethnic_groups = models.CharField(verbose_name='民族',default='汉',max_length=20)
    address = models.CharField(verbose_name='地址',max_length = 20,default='无')
    tele = models.CharField(verbose_name='联系电话',max_length=20,default='无')
    position = models.CharField(verbose_name='岗位',max_length=10,default='待入职')
    #是否为管理员——由user表中is_superuser决定
    Is_manage = models.BooleanField(verbose_name='是否为管理员',default=False)
    brief_introduction = models.CharField(verbose_name='简介',blank=True,null=True,max_length=500)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = '职员表'


class Child(models.Model):

    num = models.CharField(verbose_name='身份证号',max_length=18,blank=False,unique=True,null=False,primary_key=True)
    name = models.CharField(verbose_name='姓名',max_length=20,blank=False,null=False)
    gender = models.CharField(verbose_name='性别',max_length=5,blank=False,null=False)
    age = models.IntegerField(verbose_name='年龄',default=0,blank=False,null=False)
    edu = models.CharField(verbose_name='教育水平',default='文盲',max_length=20)
    enter_time = models.DateField(verbose_name='入院时间',default='2000.1.1',blank=False,null=False)
    weight = models.DecimalField(verbose_name='体重/kg',max_digits=5,decimal_places=2,default=0)
    height = models.DecimalField(verbose_name='身高/cm',max_digits=5,decimal_places=2,default=0)
    temperature = models.DecimalField(verbose_name='体温',max_digits=5,decimal_places=2,default=0)
    right_sight = models.DecimalField(verbose_name='右眼视力',max_digits=5,decimal_places=2,default=0)
    left_sight = models.DecimalField(verbose_name='左眼视力',max_digits=5,decimal_places=2,default=0)
    Is_adopted = models.BooleanField(verbose_name='已被领养',default=False)

    employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = '儿童表'


class To_doList(models.Model):

    content = models.CharField(verbose_name='内容',max_length=500,blank=False,null=False)
    Is_completed = models.BooleanField(verbose_name='是否完成',default=False)
    Is_read = models.BooleanField(verbose_name='是否已阅',default=False)
    topic = models.CharField(verbose_name='主题',max_length=500,blank=False,null=False,default="事件")
    #发布者为管理员/或自己
    publisher = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='publisher')

    #针对某个员工的工作安排
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employee')


    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = '待办表'

class Audit(models.Model):

    num = models.CharField(verbose_name='申请编号', max_length=18, blank=False, unique=True, null=False, primary_key=True)
    content = models.CharField(verbose_name='内容', max_length=500, blank=False, null=False)
    Is_audited = models.BooleanField(verbose_name='是否已审核', default=False)
    #可能是外人可能是员工
    #外人填身份证号，员工/儿童填num
    applicant = models.CharField(verbose_name='申请者', max_length=18, blank=False, null=False,default="申请者")

    #管理员审核通过
    manager = models.ForeignKey(Employee,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = '审核表'

class Step_parent(models.Model):

    num = models.CharField(verbose_name='身份证号', max_length=18, blank=False, unique=True, null=False, primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=20, blank=False, null=False)
    gender = models.CharField(verbose_name='性别', max_length=5, blank=False, null=False)
    age = models.IntegerField(verbose_name='年龄', default=0, blank=False, null=False)
    edu = models.CharField(verbose_name='学历', max_length=20)
    weight = models.DecimalField(verbose_name='月收入', max_digits=6, decimal_places=2, default=0)
    married = models.BooleanField(verbose_name='是否已婚',default=False,blank=False,null=False)
    Has_child = models.BooleanField(verbose_name='是否已有子女',default=False,blank=False,null=False)
    address = models.CharField(verbose_name='地址',max_length = 20,default='无')
    tele = models.CharField(verbose_name='联系电话',max_length=20,default='无')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = '领养人资料表'