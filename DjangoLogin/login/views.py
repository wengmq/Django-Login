from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.

def index(request):
    pass
    return render(request,'login/index.html')

def login(request):
    pass
    return render(request,'login/login.html')


def register(request):
    pass
    return render(request,'register/index.html')


def loginout(request):
    pass
    return render(request,'loginout/index.html')