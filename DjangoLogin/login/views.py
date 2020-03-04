from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
# Create your views here.

def index(request):
    pass
    return render(request,'login/index.html')

def login(request):
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

            if user.password == password:
                print(username, password)
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
    login_form = forms.UserForm()
    return render(request, 'login/login.html',locals())


def register(request):
    pass
    return render(request,'register/index.html')


def loginout(request):
    pass
    return render(request,'loginout/index.html')