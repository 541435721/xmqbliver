# coding:utf-8

from django.http import HttpResponse
from webuser.forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Webuser
from django.shortcuts import render, render_to_response, redirect, get_object_or_404


# Create your views here.

def index(request):
    return HttpResponse('hello')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'webuser/register.html', {'form': form})
            # return HttpResponse('表单非法')
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            hospital = form.cleaned_data.get('hospital')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            webUser = Webuser(user=user, hospital=hospital)
            webUser.save()
            login(request, user)
            return HttpResponse('注册成功！')
    else:
        return render(request, 'webuser/register.html', {'sign_up_form': SignUpForm()})


def weblogin(request):
    if request.user.is_authenticated():
        return render(request, 'webuser/loginsuccess.html')
    if request.method == "POST":
        form = LoginForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            Webuser.objects.filter(user=user).update(online=1)
            # Webuser.objects.filter(user=user).update(online=1)
            state = Webuser.objects.filter(user=user)[0].online

            return HttpResponse(u'登录状态:' + unicode(state) + u'<br>成功登录<br><a href="../logout">退出</a>')
        else:
            return render(request, 'webuser/login.html', {'form': form})
    else:
        return render(request, 'webuser/login.html', {'form': LoginForm()})


def weblogout(request):
    user=request.user
    Webuser.objects.filter(user=user).update(online=0)
    state = Webuser.objects.filter(user=user)[0].online
    logout(request)
    # return HttpResponse(u'登录状态:' + unicode(state)+u'退出')
    return render(request, 'webuser/logout.html')