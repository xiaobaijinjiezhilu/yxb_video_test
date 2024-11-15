from django.contrib.auth import logout
from django.views.generic import View
from yxb_app.libs.base_render import render_to_response
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from yxb_app.utils.permission import client_auth
from yxb_app.model.auth import ClientUser
from yxb_app.utils.consts import COOKIE_NAME


class User(View):
    TEMPLATE = 'client/auth/user.html'

    def get(self, request):

        user = client_auth(request)
        data = {
            'user': user
        }
        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not all([username, password]):
            error = '缺少必要字段'
            return JsonResponse({'code': -1, 'msg': error})
        print(username, password, '----------')
        user = ClientUser.get_user(username, password)
        print(user, 'user-----------------')
        if not user:
            error = '用户名或密码错误，未找到该用户'
            return JsonResponse({'code': -1, 'msg': error})

        response = render_to_response(request, self.TEMPLATE)
        response.set_cookie(COOKIE_NAME, str(user.id))
        return response


class Register(View):
    TEMPLATE = 'client/auth/register.html'

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not all([username, password]):
            error = '缺少必要字段'
            return JsonResponse({'code': -1, 'msg': error})

        exists = ClientUser.objects.filter(username=username).exists()
        if exists:
            error = '用户名已存在'
            return JsonResponse({'code': -1, 'msg': error})

        ClientUser.add(username=username, password=password)
        return JsonResponse({'code': 0, 'msg': '注册成功，请您登录'})


class LoginOut(View):
    TEMPLATE = 'client/auth/user.html'

    def get(self, request):
        response = render_to_response(request, self.TEMPLATE)
        response.set_cookie(COOKIE_NAME, '')
        print(request.path, 'request.path=============================')

        return response
