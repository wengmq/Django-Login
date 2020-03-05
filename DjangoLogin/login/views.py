from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import datetime
from django.conf import settings
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

            #判断用户的账号是否是邮件确认过
            if not user.has_confiremed:
                message = '该用户还未经过邮件确认'
                return render(request,'login/login.html',locals())

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

    # 第一次进入登陆界面，把把表单样式传给前端的html
    login_form = forms.UserForm()
    return render(request, 'login/login.html',locals())

# 生成一个唯一的确认码
    # make_confirm_string()方法接收一个用户对象作为参数。
    # 首先利用datetime模块生成一个当前时间的字符串now，
    # 再调用我们前面编写的hash_code()方法以用户名为基础，now为‘盐’，
    # 生成一个独一无二的哈希值，再调用ConfirmString模型的create()方法，
    # 生成并保存一个确认码对象。最后返回这个哈希值。
def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code


# 发送邮件
    # 首先我们需要导入settings配置文件from django.conf import settings。
    # 邮件内容中的所有字符串都可以根据你的实际情况进行修改。
    # 其中关键在于<a href=''>中链接地址的格式，
    # 我这里使用了硬编码的'127.0.0.1:8000'，请酌情修改，
    # url里的参数名为code，它保存了关键的注册确认码，
    # 最后的有效期天数为设置在settings中的CONFIRM_DAYS。
    # 所有的这些都是可以定制的！
def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.wengmq.top的注册确认邮件'

    text_content = '''感谢注册www.wengmq.top，\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.wengmq.top</a></p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("向{}发送邮件成功！".format(email))

# 处理邮件确认请求
    # 通过request.GET.get('code', None)从请求的url地址中获取确认码;
    # 先去数据库内查询是否有对应的确认码;
    # 如果没有，返回confirm.html页面，并提示;
    # 如果有，获取注册的时间c_time，加上设置的过期天数，
    # 这里是7天，然后与现在时间点进行对比；
    # 如果时间已经超期，删除注册的用户，同时注册码也会一并删除，
    # 然后返回confirm.html页面，并提示;
    # 如果未超期，修改用户的has_confirmed字段为True，并保存，
    # 表示通过确认了。然后删除注册码，但不删除用户本身。
    # 最后返回confirm.html页面，并提示。
def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        # confirm.user.has_confirmed = True
        # confirm.user.save()

        user = models.User.objects.get(name=confirm.user.name)
        user.has_confiremed = True
        user.save()

        #delete掉ConfirmString中的数据下次再访问邮箱里面的确认的链接，就会失效
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())

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

                #发送邮件确认
                code = make_confirm_string(new_user)
                send_email(email,code)

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