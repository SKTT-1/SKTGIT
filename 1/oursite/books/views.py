#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from books.models import User,Things

# Create your views here.
def log(request):
    return render_to_response('log.html')
def login(request):
    if "username" in request.session:
            u=User.objects.get(UserName=request.session["username"])
            if u.Level=='1':
                Level="计算机"
            if u.Level=='2':
                Level="家具"
            if u.Level=='3':
                Level="仪器"
            dic={'name':u.UserName,
                 'level':Level}
            return render_to_response('mainpage.html',dic)
    if request.POST['p'] and request.POST['q']:
        user=request.POST['p']
        psw=request.POST['q']
        if  User.objects.filter(UserName=user,PassWord=psw):
            u=User.objects.get(UserName=user)
            request.session["username"]=user
            request.session["level"]=u.Level
            if u.Level=='1':
                Level="计算机"
            if u.Level=='2':
                Level="家具"
            if u.Level=='3':
                Level="仪器"
            dic={'name':u.UserName,
                 'level':Level}
            return render_to_response('mainpage.html',dic)
        else:
            return HttpResponse("Please input the right UserName or PassWord!")
    else:
        
        return HttpResponse("Please input the right UserName or PassWord!")
def add(request):
    return render_to_response('addpeople.html')
def addpeople(request):
    name=request.POST['p']
    psw=request.POST['q']
    rpsw=request.POST['j']
    level=request.POST['k']
    if name and rpsw and psw and level:
        if User.objects.filter(UserName=name):
            return HttpResponse("The User already exists!")
        else:
            if rpsw!=psw:
                return HttpResponse("Please input the same password!")
            else:
                if level>='1' and level<='3':
                    p=User(UserName=name,PassWord=psw,Level=level)
                    p.save()
                    return HttpResponse("Congratulations!You are one of us now!")
                else:
                    return HttpResponse("Please input the right level!")
    else:
        return HttpResponse("The massage can't be blank!")
def add1(request):
    return render_to_response("addf.html")
def addf(request):
    name1=request.POST['p']
    ID=request.POST['q']
    Type=request.POST['j']
    Date=request.POST['k']
    if Things.objects.filter(Name=name1):
        return HttpResponse("设备已经存在！")
    else:
        if name1 and ID and Type and Date:
            p=Things(Level=request.session["level"],Name=name1,FID=ID,Xing=Type,BDate=Date,S='3')
            p.save()
            return HttpResponse("保存成功！")
        else:
            return HttpResponse("信息不能为空!")
def searchform(request):
    return render_to_response("search.html")            
def search(request):
    name=request.GET['q']
    if name:
        if Things.objects.filter(Name=name,Level=request.session["level"]):
             F=Things.objects.get(Name=name)
             return render_to_response("search-results.html",{'n':F.Name})
        else:
            return HttpResponse("设备不存在！")
    else:
        return HttpResponse("设备名称不能为空！") 
def manage(request):
    n=request.GET['name']
    F=Things.objects.get(Name=n)
    F.S='1'
    F.save()
    return HttpResponse("已标记借出！")
def manage1(request):
    n=request.GET['name']
    F=Things.objects.get(Name=n)
    F.S='2'
    F.save()
    return HttpResponse("已标记报废！")
def manage2(request):
    n=request.GET['name']
    F=Things.objects.get(Name=n)
    F.S='3'
    F.save()
    return HttpResponse("已标记正常使用！") 
def check(request):
    n=request.GET['name']        
    F=Things.objects.get(Name=n)
    if F.S=='1' or F.S=='2':
        if F.S=='1':
            s="借出中"
        if F.S=='2':
            s="已报废"
    else:
        s="使用中"

    dic={"name":F.Name,
         "ID":F.FID,
         "X":F.Xing,
         "S":s,
         "D":F.BDate
    }
    return render_to_response("check.html",dic)
def state(request):
    s1=Things.objects.filter(S__contains='1', Level=request.session["level"])
    s2=Things.objects.filter(S__contains='2', Level=request.session["level"])
    s3=Things.objects.filter(S__contains='3', Level=request.session["level"])
    Level=request.session["level"]
    if Level=='1':
        kind="计算机"
    if Level=='2':
        kind="家具"
    if Level=='3':
        kind="仪器"
    dic={'fun1':s1,
         'fun2':s2,
         'fun3':s3,
         'kind':kind
    }
    return render_to_response("state.html",dic)
def up(request):
    name=request.GET['name']
    things=Things.objects.get(Name=name)
    return render_to_response("update.html",{'things':things})
def update(request):
    n=request.POST['p']
    ID=request.POST['q']
    Type=request.POST['j']
    date=request.POST['k']
    if n and ID and Type and date:
        F=Things.objects.get(Name=n)
        F.FID=ID
        F.Xing=Type
        F.BDate=date
        F.save()
        return HttpResponse("更新成功！")
    else:
        return HttpResponse("请输入正确的信息！")
def logout(request):
    del request.session["username"]
    del request.session["level"]
    return render_to_response("logout.html")
            
        

            
