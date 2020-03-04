# Django-Login

#进入项目
cd C:\project\Django-Login

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