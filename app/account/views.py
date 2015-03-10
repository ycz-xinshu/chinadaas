#encoding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from string import Template

def sign_in(request):
    ctx = csrf(request)
    return render_to_response('account/sign_in.html', ctx)


def do_sign_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print username
    user = authenticate(username=username, password=password)
    ctx = {}
    if user:
        if user.is_active:
            login(request, user)
        else:
            ctx.update(dict(message='登录失败，原因：用户失效'))
            ctx.update(dict(retry_url='sign_in'))
            return render_to_response('index.html', ctx)
    else:
        ctx.update(dict(message='登录失败，原因：用户名密码错误'))
        ctx.update(dict(retry_url='sign_in'))
        return render_to_response('index.html', ctx)
    return HttpResponseRedirect('/')

def sign_up(request):
    ctx = csrf(request)
    return render_to_response('account/sign_up.html', ctx)


def do_sign_up(request):
    post = request.POST.dict()
    post["password"] = User.objects.make_random_password()
    del post["csrfmiddlewaretoken"]
    user = User.objects.create_user(**post)
    user.save()
    user.email_user('Chinadaas平台新用户注册', Template('用户名: $username, 密码: $password').substitute(**post), "oppps@163.com")

    return HttpResponseRedirect('/')

@login_required
def change_pwd(request):
    ctx = dict(user=request.user)
    ctx.update(csrf(request))
    return render_to_response('account/change_pwd.html', ctx)


def do_change_pwd(request):
    old_pwd = request.POST.get('oldpasswd')
    new_pwd = request.POST.get('newpasswd')
    user = request.user
    ctx = dict(user=user)
    if not user.check_password(old_pwd):
        ctx.update(dict(message='修改密码失败，原因：旧密码不正确'))
        ctx.update(dict(retry_url='change_pwd'))
        return render_to_response('error.html', ctx)
    user.set_password(new_pwd)
    user.save()
    ctx.update(dict(message='已成功修改密码'))
    return render_to_response('account/success.html', ctx)


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')
