# Django-Login

#进入项目
cd C:\project\Django-Login\DjangoLogin

#进入环境变量
C:\Users\wengmq\Virtualenv\DjangoLogin_env\Scripts\activate

#退出环境变量
deactivate

#安装依赖包
pip install -r requirements.txt
若是安装不行可以依次执行以下命令：
python -m pip install --upgrade pip
easy_install --upgrade pip

#创建项目
django-admin startproject DjangoLogin


#数据库迁移
python manage.py makemigrations
python manage.py migrate


#创建管理账号，访问http://127.0.0.1:8000/admin/
python manage.py createsuperuser


在Django中发送邮件
其实在Python中已经内置了一个smtp邮件发送模块，Django在此基础上进行了简单地封装。

首先，我们需要在项目的settings文件中配置邮件发送参数，分别如下：

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xxx@sina.com'
EMAIL_HOST_PASSWORD = 'xxxxxxxxxxx'
第一行指定发送邮件的后端模块，大多数情况下照抄！
第二行，不用说，发送方的smtp服务器地址，建议使用新浪家的；
第三行，smtp服务端口，默认为25；
第四行，你在发送服务器的用户名；
第五行，对应用户的密码。