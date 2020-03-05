from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
# Create your views here.

def index(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    return render(request,'login/index.html')

#用于加密密码存入数据库中
def hash_code(s,salt='DjangoLogin'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())# update方法只接收bytes类型
    return h.hexdigest()

def login(request):

    #使用session设置不允许重复登录
    #已经login的状态下，
    # 手动从浏览器地址栏中访问/login/也依然进入的是index页面。
    if request.session.get('is_login',None):
        return redirect('/index/')

    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        message = '请检查填写的内容！'
        # if username.strip() and password:
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')


            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                #往session字典内写入用户状态和数据
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                # print(username, password)
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    # Python内置了一个locals()函数，它返回当前所有的本地变量字典，
    # 我们可以偷懒的将这作为render函数的数据字典参数值，
    # 就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了。
    # 这样做的好处当然是大大方便了我们，但是同时也可能往模板传入了一些多余的变量数据，造成数据冗余降低效率。

    #第一次进入登陆界面，把把表单样式传给前端的html
    login_form = forms.UserForm()
    return render(request, 'login/login.html',locals())


def register(request):

    #先实例化一个RegisterForm的对象，
    # 然后使用is_valide()验证数据，
    # 再从cleaned_data中获取数据。
    #重点在于注册逻辑，首先两次输入的密码必须相同，
    # 其次不能存在相同用户名和邮箱，最后如果条件都满足，
    # 利用ORM的API，创建一个用户实例，然后保存到数据库内。

    #若已经登录，直接跳转到首页
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"

        #表单数据有效时
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())

            #匹配数据库数据
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                #写入到数据库，先新建一个models.User()对象
                new_user = models.User()
                new_user.name = username
                #在数据库中加密密码
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())

    #第一次进入注册界面，把把表单样式传给前端的html
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):

    # 如果本来就未登录，也就没有登出一说
    if not request.session.get('is_login',None):
        return redirect("/login/")

    #删除当前的会话数据和会话cookie。在用户退出后，删除会话。
    request.session.flush()
    return redirect("/login/")