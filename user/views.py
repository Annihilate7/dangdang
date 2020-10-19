import random, string

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from captcha.image import ImageCaptcha
from index.models import TUser


def login(request):
    username = request.COOKIES.get('username')
    password = request.COOKIES.get('password')
    if TUser.objects.filter(user_name=username, password=password):
        request.session['username'] = username
        return redirect('index:index')
    page = request.GET.get('page')
    if page:
        return render(request, 'login.html', {'page': page})
    return render(request, 'login.html', {'page': '/index/'})


def captcha(request):
    img = ImageCaptcha()
    code_list = random.sample(string.ascii_letters + string.digits, 4)
    code = ''.join(code_list)
    data = img.generate(code)
    request.session['code'] = code
    return HttpResponse(data, 'image/png')


def login_logic(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    captcha = request.POST.get('captcha')
    code = request.session.get('code')
    print(username, password, captcha, code)
    if TUser.objects.filter(user_name=username, password=password) and code.lower() == captcha.lower():
        response = HttpResponse('yes')
        request.session['username'] = username
        print(request.POST.get('check'))
        if request.POST.get('check') == 'true':
            response.set_cookie('username', username, max_age=7 * 24 * 60 * 60)
            response.set_cookie('password', password, max_age=7 * 24 * 60 * 60)
            return response
        return response
    return HttpResponse('no')


def register(request):
    page = request.GET.get('page')
    if page:
        return render(request, 'register.html', {'page': page})
    return render(request, 'register.html', {'page': '/index/'})


def check_user(request):
    username = request.POST.get('username')
    if TUser.objects.filter(user_name=username):
        return JsonResponse({'ready': 'yes'})
    return JsonResponse({'ready': 'no'})


def check_captcha(request):
    captcha = request.POST.get('captcha')
    code = request.session.get('code')
    if code.lower() == captcha.lower():
        return HttpResponse('yes')
    return HttpResponse('no')


def register_logic(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    captcha = request.POST.get('captcha')
    code = request.session.get('code')
    if not TUser.objects.filter(user_name=username) and code.lower() == captcha.lower():
        request.session['username'] = username
        with transaction.atomic():
            TUser.objects.create(user_name=username, password=password)
        return JsonResponse({'ready': 'yes'})
    return JsonResponse({'ready': 'no'})


def register_ok(request):
    page = request.GET.get('page')
    username = request.GET.get('username')
    request.session['username'] = username
    return render(request, 'register ok.html', {'username': username, 'page': page})


def quit(request):
    username = request.COOKIES.get('username')
    password = request.COOKIES.get('password')
    response = HttpResponse('quit')
    response.set_cookie('username', username, max_age=0)
    response.set_cookie('password', password, max_age=0)
    request.session.flush()
    return response