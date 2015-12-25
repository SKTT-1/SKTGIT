# -*- coding: utf-8 -*-
from extend.models import *
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect
import time
# Create your views here.
def authority(request):
    try:
        usertemp = User.objects.get(Acount=request.session['acount'])
        if request.session['password']==usertemp.Password:
            return 1
        else:
            return 0
    except:
        return 0
def admin_authority(request):
    if authority(request) :
        usertemp = User.objects.get(Acount=request.session['acount'])
        if usertemp.Level == u'0':
            return 1
        else:
            return 0
    else:
        return 0
def user_authority(request):
    if authority(request) :
        usertemp = User.objects.get(Acount=request.session['acount'])
        if usertemp.Level != u'0':
            return 1
        else:
            return 0
    else:
        return 0
        

def login(request):
    if request.POST :
        post = request.POST
        try:
            if "acount" in request.session :
                del request.session["acount"]
                del request.session["password"]
                del request.session["level"]
            if post['password']==User.objects.get(Acount = post['acount']).Password:
                userinform = User.objects.get(Acount=post['acount'])
                request.session["acount"]=userinform.Acount
                request.session["password"]=userinform.Password
                request.session["level"]=userinform.Level
                return HttpResponseRedirect('/homepage')
            else:
                fail = 1
                return render_to_response("index.html",Context({"fail":fail,}))
        except:
            fail = 1 
            return render_to_response("index.html",Context({"fail":fail,}))
    fail = 0
    return render_to_response("index.html",Context({"fail":fail,}))
def show_homepage(request):
    if authority(request):
        user =User.objects.get(Acount=request.session['acount'])
        if user.Level == '0' :
            return render_to_response("homepage_admin.html",Context({"Username":user.Name,}))
        else:
            Level="计算机"
            if user.Level == '1' :
                Level="计算机"
            if user.Level == '2' :
                Level="家具"
            if user.Level == '3' :
                Level="仪器"
            return render_to_response("homepage_user.html",Context({"Username":user.Name,"kind":Level,}))
    else:
        return render_to_response("user_error.html")
def log_out(request):
    if "acount" in request.session :
        del request.session["acount"]
        del request.session["password"]
        del request.session["level"]
    return HttpResponseRedirect('/')
    
    
#admin function
def check_user(request):
    if admin_authority(request):
        usertemp = User.objects.get(Acount=request.session['acount'])
        user_list = User.objects.exclude(Level = '0')
        isnull = 0
        try:
            user_list[0]
        except:
            isnull = 1  
        return render_to_response("check_user.html",Context({"user_list":user_list,"isnull":isnull,"Username":usertemp.Name,}))
    else:
        return render_to_response("user_error.html")
def add_user(request):
    if admin_authority(request):
        if request.POST :
            post = request.POST
            try: 
                User.objects.get(acount = post["acount"])
                return HttpResponse("此用户已经存在！")
            except:
                if post["acount"]=='' or post["password"]=='' or post["name"]=='' or post["belong"]=='':
                    error = 1
                    return render_to_response("add_user.html",Context({"error":error,}))
                elif post["password"] == post["passwordcheck"]:
                    new_user = User(
                    Level = post["level"],
                    Acount = post["acount"],
                    Password = post["password"],
                    Name = post["name"],
                    Belong = post["belong"],)
                    new_user.save()
                    return HttpResponseRedirect('/check_user')
                else:
                    error = 2
                    return render_to_response("add_user.html",Context({"error":error,}))
        error=0
        return render_to_response("add_user.html",Context({"error":error,}))
    else:
        return render_to_response("user_error.html")

def manage_form(request):
    if admin_authority(request):
        addform_list = AddForm.objects.filter(State = "申请中")
        form_list = Form.objects.filter(State = "申请中")
        form_list1 = Form.objects.filter(State = "归还申请")
        form_list = form_list|form_list1
        return render_to_response("manage_form.html",Context({"addform_list":addform_list,"form_list":form_list,}))
    else:
        return render_to_response("user_error.html")
def add_apply(request):
    if admin_authority(request):
        if request.POST :
            addform = AddForm.objects.get(Formnumber = request.GET["form"])
            addform.Suggestion = request.POST["suggestion"]
            if request.POST.has_key('agree'):
                addform.State = "同意"
                for i in range(int(addform.Amount)):
                    new_device = Device(
                    Level = addform.Level,
                    Kind = addform.Kind,
                    Name = addform.Name,
                    Date = addform.Date,
                    Formatx = addform.Formatx,
                    Price = addform.Price,
                    State = "正常",
                    )
                    new_device.save()
                addform.save()
            elif request.POST.has_key('disagree'):
                addform.State = "不同意"
                addform.save()
            return HttpResponseRedirect("/manage_form/")
        addform = AddForm.objects.get(Formnumber = request.GET["form"])
        judge = 0
        if addform.State != u"申请中":
            judge = 1
        if addform.State == u"删除":
            judge = 2
        user = User.objects.get(Acount = addform.Applicant)
        return render_to_response("add_apply.html",Context({"addform":addform,"judge":judge,"user":user,}))
    else:
        return render_to_response("user_error.html")
def show_addform(request):
    if admin_authority(request):
        addform_list = AddForm.objects.all()
        return render_to_response("show_addform.html",Context({"addform_list":addform_list,}))
    else:
        return render_to_response("user_error.html")
def manage_apply(request):
    if admin_authority(request):
        formnumber = request.GET["form"]
        if request.POST :
            if request.POST.has_key("agree"):
                post = request.POST
                if Form.objects.get(Formnumber = post["form"]).State == u"归还申请":
                    device_list = Device.objects.filter(Form = post["form"])
                    for device in device_list:
                        device.State = "正常"
                        device.Borrower = ""
                        device.save()
                    form = Form.objects.get(Formnumber = post["form"])
                    form.State = "归还成功"
                    form.save()
                else:
                    action = post["action"]
                    device_list = Device.objects.filter(Form = post["form"])
                    for device in device_list:
                        device.State = action
                        if action == u"借出":
                            device.Borrower = post["applicant"]
                        device.save()
                    form = Form.objects.get(Formnumber = post["form"])
                    form.State = "同意"
                    form.Suggestion = post["suggestion"]
                    form.save()
            elif request.POST.has_key("disagree"):
                post = request.POST
                if Form.objects.get(Formnumber = post["form"]).State == u"归还申请":
                    form = Form.objects.get(Formnumber = post["form"])
                    form.State = "归还失败"
                    form.save()
                else:
                    action = post["action"]
                    device_list = Device.objects.filter(Form = post["form"])
                    for device in device_list:
                        device.State = "正常"
                        device.Form = 0
                        device.save()
                    form = Form.objects.get(Formnumber = post["form"])
                    form.State = "不同意"
                    form.Suggestion = post["suggestion"]
                    form.save()
            elif request.POST.has_key("delete"):
                device_list = Device.objects.filter(Form = request.GET["form"])
                for device in device_list:
                    device.State = "正常"
                    device.Form = 0
                    device.save()
                form = Form.objects.get(Formnumber = formnumber)
                form.State = "删除"
                form.save()
        form = Form.objects.get(Formnumber = formnumber)
        judge = 0
        if form.State != u"申请中":
            judge = 2
        if form.State == u"归还申请":
            judge = 1
        if form.State ==u"初始":
            judge = 3
        if form.State ==u"删除":
            judge = 4
        username = User.objects.get(Acount = request.session["acount"])
        user = User.objects.get(Acount = form.Applicant)
        return render_to_response("manage_apply.html",Context({"form":form,"judge":judge,"Username":username,"user":user,}))
    else:
        return render_to_response("user_error.html")
def show_form(request):
    if admin_authority(request):
        form_list = Form.objects.all()
        return render_to_response("show_form.html",Context({"form_list":form_list,}))
    else:
        return render_to_response("user_error.html")
def updata_user(request):
    if admin_authority(request):
        acount = request.GET["Acount"]
        user = User.objects.get(Acount = acount)
        error = 0
        if request.POST :
            post = request.POST
            if post["password"] == '' :
                error = 1
                return render_to_response("updata_user.html",Context({"user":user,"error":error,}))
            if post["password"] == post["checkpass"]:
                user.Password = post["password"]
                user.save()
                return HttpResponseRedirect("/check_user/")
            elif post["password"] != post["checkpass"]:
                error = 2
                return render_to_response("updata_user.html",Context({"user":user,"error":error,}))
        return render_to_response("updata_user.html",Context({"user":user,"error":error,}))
    else:
        return render_to_response("user_error.html")
def delete_user(request):
    if admin_authority(request):
        acount = request.GET["Acount"]
        device_list = Device.objects.filter(Borrower = acount)
        for device in device_list:
            device.State = "正常"
            device.Borrower = ""
            device.Form = 0
            device.save()
        user = User.objects.get(Acount = acount)
        user.delete()
        return HttpResponseRedirect("/check_user/")
    else:
        return render_to_response("user_error.html")
def user_inform(request):
    if admin_authority(request):
        user = User.objects.get(Acount = request.GET["acount"])
        return render_to_response("user_inform.html",Context({"user":user,}))
    else:
        return render_to_response("user_error.html")
def check_device(request):
    if admin_authority(request):
        if request.method == "POST":
            device_list = Device.objects.all()
            user = User.objects.get(Acount = request.session["acount"])
            if request.POST.has_key('search'): 
                post = request.POST
                search = Device(
                Kind = post["kind"],
                Level = post["level"],
                Name = post["name"],
                Date = post["date"],
                Price = post["price"],
                State = post["state"],
                Borrower = post["borrower"],
                )
                request.session["admin_device"] = search
                return HttpResponseRedirect('/check_device/')
        user = User.objects.get(Acount = request.session["acount"])
        device_list = Device.objects.all()
        try:
            search = request.session["admin_device"]
            if search.Kind !='':
                device_list = device_list.filter(Kind = search.Kind)
            if search.Level !='':
                device_list = device_list.filter(Level = search.Level)
            if search.Name !='':
                device_list = device_list.filter(Name = search.Name)
            if search.Date !='':
                device_list = device_list.filter(Date = search.Date)
            if search.Price!='':
                device_list = device_list.filter(Price = search.Price)
            if search.State!='':
                device_list = device_list.filter(State = search.State)
            if search.Borrower!='':
                device_list = device_list.filter(Borrower = search.Borrower)
        except:
            search = Device()
        judge = 0
        if search.State == u"正常":
            judge = 1
        if search.State == u"借出":
            judge = 2
        if search.State == u"报废":
            judge = 3
        return render_to_response("check_device.html",Context({"device_list":device_list,
        "Username":user.Name,"search":search,"request":request,"judge":judge,}))
    else:
        return render_to_response("user_error.html") 
        
        
        
#user function
def my_inform(request):
    if user_authority(request):
        user = User.objects.get(Acount = request.session["acount"])
        return render_to_response("my_inform.html",Context({"user":user}))
    else:
        return render_to_response("user_error.html")
def change_passwd(request):
    if user_authority(request):
        acount = request.session["acount"]
        user = User.objects.get(Acount = acount)
        error = 0
        if request.POST :
            post = request.POST
            if post["old_password"] != user.Password:
                error = 3
                return render_to_response("change_passwd.html",Context({"user":user,"error":error,}))
            if post["password"] == '' :
                error = 1
                return render_to_response("change_passwd.html",Context({"user":user,"error":error,}))
            if post["password"] == post["checkpass"]:
                user.Password = post["password"]
                user.save()
                return render_to_response("change_success.html")
            elif post["password"] != post["checkpass"]:
                error = 2
                return render_to_response("change_passwd.html",Context({"user":user,"error":error,}))
        return render_to_response("change_passwd.html",Context({"user":user,"error":error,}))
    else:
        return render_to_response("user_error.html")
def search_device(request):
    if user_authority(request):
        if request.method == "POST":
            device_list = Device.objects.filter(Level = request.session["level"])
            user = User.objects.get(Acount = request.session["acount"])
            if request.POST.has_key('search'): 
                post = request.POST
                search = Device(
                Kind = post["kind"],
                Name = post["name"],
                Date = post["date"],
                Price = post["price"],
                State = post["state"],
                Borrower = post["borrower"],
                )
                request.session["device"] = search
                return HttpResponseRedirect('/search_device/')
            if request.POST.has_key('borrow'): 
                chk_list = request.REQUEST.getlist('chk')
                if len(chk_list) == 0:
                    return HttpResponse("没有设备被选中！")
                mark = 0
                for i in range(len(chk_list)):
                    if Device.objects.get(SN = chk_list[i]).State != u"正常":
                        mark = 1
                if mark == 0:
                    new_form = Form(
                    Level = request.session["level"],
                    Action = "借出",
                    Applicant = request.session["acount"],
                    Amount = len(chk_list),
                    Reason = "",
                    State = "初始",
                    Date = time.strftime('%Y-%m-%d',time.localtime(time.time())),
                    Suggestion = "",
                    )
                    new_form.save()
                    for i in range(len(chk_list)):
                        device = Device.objects.get(SN = chk_list[i])
                        device.Form = int(new_form.Formnumber)
                        device.State = "借出申请中"
                        device.Borrower = request.session["acount"]
                        device.save()
                    return HttpResponseRedirect("/borrow_apply/?form="+str(new_form.Formnumber))
                else:
                    return HttpResponse("含有被占用设备！")
            if request.POST.has_key('dumping'): 
                chk_list = request.REQUEST.getlist('chk')
                if len(chk_list) == 0:
                    return HttpResponse("没有设备被选中！")
                mark = 0
                for i in range(len(chk_list)):
                    if Device.objects.get(SN = chk_list[i]).State != u"正常":
                        mark = 1
                if mark == 0:
                    new_form = Form(
                    Level = request.session["level"],
                    Action = "报废",
                    Applicant = request.session["acount"],
                    Amount = len(chk_list),
                    Reason = "",
                    State = "初始",
                    Date = time.strftime('%Y-%m-%d',time.localtime(time.time())),
                    Suggestion = "",
                    )
                    new_form.save()
                    for i in range(len(chk_list)):
                        device = Device.objects.get(SN = chk_list[i])
                        device.Form = int(new_form.Formnumber)
                        device.State = "报废申请中"
                        device.save()
                    return HttpResponseRedirect("/dumping_apply/?form="+str(new_form.Formnumber))
                else:
                    return HttpResponse("含有被占用设备！")
        user = User.objects.get(Acount = request.session["acount"])
        Level ="计算机"
        if user.Level == '1' :
            Level="计算机"
        if user.Level == '2' :
            Level="家具"
        if user.Level == '3' :
            Level="仪器"
        device_list = Device.objects.filter(Level = request.session["level"])
        try:
            search = request.session["device"]
            if search.Kind !='':
                device_list = device_list.filter(Kind = search.Kind)
            if search.Name !='':
                device_list = device_list.filter(Name = search.Name)
            if search.Date !='':
                device_list = device_list.filter(Date = search.Date)
            if search.Price!='':
                device_list = device_list.filter(Price = search.Price)
            if search.State!='':
                device_list = device_list.filter(State = search.State)
            if search.Borrower!='':
                device_list = device_list.filter(Borrower = search.Borrower)
        except:
            search = Device()
        judge = 0
        if search.State == u"正常":
            judge = 1
        if search.State == u"借出":
            judge = 2
        if search.State == u"报废":
            judge = 3
        return render_to_response("search_device.html",Context({"device_list":device_list,
        "Username":user.Name,"search":search,"Userkind":Level,"request":request,"judge":judge,}))
    else:
        return render_to_response("user_error.html")
def add_device(request):
    if user_authority(request):
        if request.POST :
            post = request.POST
            new_form = AddForm(
            Applicant = request.session["acount"],
            Level = request.session["level"],
            Kind = post["kind"],
            Name = post["name"],
            Date = post["date"],
            Formatx = post["formatx"],
            Price = post["price"],
            Amount = post["amount"],
            Reason = post["reason"],
            State = "申请中",
            Suggestion = ""
            )
            new_form.save()
            return HttpResponseRedirect("/homepage")
        return render_to_response("add_device.html")
    else:
        return render_to_response("user_error.html")
def borrow_apply(request):
    if user_authority(request):
        if request.POST :
            post = request.POST
            form = Form.objects.get(Formnumber = post["formnumber"])
            form.Reason = post["reason"]
            form.State = "申请中"
            form.save()
            return HttpResponseRedirect("/search_device")
        try:
            SNtemp = request.GET["SN"]
            device = Device.objects.get(SN= SNtemp)
            if device.State == u"正常":
                device.State = "借出申请中"
                new_form = Form(
                Level = request.session["level"],
                Action = "借出",
                Applicant = request.session["acount"],
                Amount = '1',
                Reason = "",
                Date = time.strftime('%Y-%m-%d',time.localtime(time.time())),
                State = "初始",
                Suggestion = "",
                )
                new_form.save()
                device.Form = new_form.Formnumber
                device.save()
                return render_to_response("borrow_apply.html",Context({"form":new_form,}))
            else:
                return HttpResponse("此设备已占用！")
        except:
            formtemp = request.GET["form"]
            form = Form.objects.get(Formnumber = formtemp)
            return render_to_response("borrow_apply.html",Context({"form":form,}))
    else:
        return render_to_response("user_error.html")
def dumping_apply(request):
    if user_authority(request):
        if request.POST :
            post = request.POST
            form = Form.objects.get(Formnumber = post["formnumber"])
            form.Reason = post["reason"]
            form.State = "申请中"
            form.save()
            return HttpResponseRedirect("/search_device")
        try:
            SNtemp = request.GET["SN"]
            device = Device.objects.get(SN= SNtemp)
            if device.State == u"正常":
                device.State = "报废申请中"
                new_form = Form(
                Level = request.session["level"],
                Action = "报废",
                Applicant = request.session["acount"],
                Amount = '1',
                Reason = "",
                Date = time.strftime('%Y-%m-%d',time.localtime(time.time())),
                State = "初始",
                Suggestion = "",
                )
                new_form.save()
                device.Form = new_form.Formnumber
                device.save()
                return render_to_response("dumping_apply.html",Context({"form":new_form,}))
            else:
                return HttpResponse("此设备已占用！")
        except:
            formtemp = request.GET["form"]
            form = Form.objects.get(Formnumber = formtemp)
            return render_to_response("dumping_apply.html",Context({"form":form,}))
    else:
        return render_to_response("user_error.html")
def myform(request):
    if user_authority(request):
        useracount = request.session["acount"]
        level = request.session["level"]
        username = User.objects.get(Acount = useracount)
        Level="计算机"
        if level == '1' :
            Level="计算机"
        if level == '2' :
            Level="家具"
        if level == '3' :
            Level="仪器"
        addform_list = AddForm.objects.filter(Applicant = useracount)
        form_list = Form.objects.filter(Applicant = useracount)
        return render_to_response("myform.html",Context({"addform_list":addform_list,"form_list":form_list,"Level":Level,"Username":username,}))
    else:
        return render_to_response("user_error.html")
def user_addform(request):
    if user_authority(request):
        addform = AddForm.objects.get(Formnumber = request.GET["form"])
        if request.POST.has_key("delete"):
            device_list = Device.objects.filter(Form = request.GET["form"])
            for device in device_list:
                device.State = "正常"
                device.Form = 0
                device.save()
            addform.State = "删除"
            addform.save()
            return HttpResponseRedirect("/user_addform/?form="+str(request.GET["form"]))
        
        judge = 0
        if addform.State == u"申请中":
            judge = 1
        if addform.State == u"删除":
            judge = 2
        user = User.objects.get(Acount = request.session["acount"])
        return render_to_response("user_addform.html",Context({"form":addform,"judge":judge,"Username":user,}))
    else:
        return render_to_response("user_error.html")
def user_form(request):
    if user_authority(request):
        form = Form.objects.get(Formnumber = request.GET["form"])
        if request.POST:
            if request.POST.has_key("giveback"):
                form.State = "归还申请"
                form.save()
            if request.POST.has_key("give"):
                form.State = "申请中"
                form.Reason = request.POST["reason"]
                form.save()
            if request.POST.has_key("delete"):
                device_list = Device.objects.filter(Form = request.GET["form"])
                for device in device_list:
                    device.State = "正常"
                    device.Form = 0
                    device.save()
                form.State = "删除"
                form.save()
            return HttpResponseRedirect("/user_form/?form="+str(request.GET["form"]))
        judge = 0
        if form.State == u"申请中":
            judge = 1
        if form.State == u"初始":
            judge = 2
        if form.Action == u"借出" and form.State == u"同意":
            judge = 3
        if form.State == u"归还失败" :
            judge = 4
        if form.State == u"删除":
            judge = 5
        user = User.objects.get(Acount = request.session["acount"])
        return render_to_response("user_form.html",Context({"form":form,"judge":judge,"Username":user,}))
    else:
        return render_to_response("user_error.html")
def show_device(request):
    urlpath = request.path
    method = urlpath.split('/')[1]
    formnumber = request.GET["form"]
    device_list = Device.objects.filter(Form = formnumber)
    judge = 0
    if user_authority(request):
        if method == "form_inform":
            judge = 0
            return render_to_response("show_device.html",Context({"device_list":device_list,"formnumber":formnumber,"judge":judge,}))
        if method == "check_borrow":
            judge = 1
            return render_to_response("show_device.html",Context({"device_list":device_list,"formnumber":formnumber,"judge":judge,}))
        if method == "check_dumping":
            judge = 2
            return render_to_response("show_device.html",Context({"device_list":device_list,"formnumber":formnumber,"judge":judge,}))
        return render_to_response("user_error.html")
    elif admin_authority(request):
        if method == "check_manage":
            judge = 3
            return render_to_response("show_device.html",Context({"device_list":device_list,"formnumber":formnumber,"judge":judge,}))
        return render_to_response("user_error.html")
    else:
        return render_to_response("user_error.html")
        
    
    
    