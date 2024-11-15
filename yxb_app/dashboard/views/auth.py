from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from yxb_app.libs.base_render import render_to_response
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
# 分页
from django.core.paginator import Paginator
from yxb_app.utils.permission import dashboard_auth
from yxb_app.model.auth import ClientUser
from django.http import JsonResponse


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        return render_to_response(request, self.TEMPLATE)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        to = request.GET.get('to', '')

        data = {}

        exists = User.objects.filter(username=username).exists()
        data['error'] = '没有该用户'
        if not exists:
            return render_to_response(request, self.TEMPLATE, data)
        user = authenticate(username=username, password=password)

        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data=data)

        if not user.is_superuser:
            data['error'] = '你无权登录'
            return render_to_response(request, self.TEMPLATE, data=data)
        user = authenticate(username=username, password=password)
        print(user, '登陆成功')
        login(request, user)

        if to:
            return redirect(to)

        return redirect(reverse('dashboard_index'))


class Register(View):
    TEMPLATE = 'dashboard/auth/register.html'

    def get(self, request):
        return render_to_response(request, self.TEMPLATE)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        check_password = request.POST.get('check_password')
        print(username, password)
        if password != check_password:
            return redirect('/register?error=密码不相同')

        exists = User.objects.filter(username=username).exists()
        if exists:
            return redirect('/register?error=该用户已存在')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect(reverse('dashboard_login'))


class AdminManger(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        users = User.objects.all().order_by('id')
        page = request.GET.get('page', 1)
        p = Paginator(users, 6)
        total_page = p.num_pages
        if int(page) <= 1:
            page = 1
        current_page = p.get_page(int(page)).object_list

        data = {'users': current_page, 'total': total_page, 'page_num': int(page)}
        return render_to_response(request, self.TEMPLATE, data=data)


class LogOut(View):
    def get(self, request):
        logout(request)

        return redirect(reverse('dashboard_login'))


class AdminUpdateStatus(View):

    def get(self, request):
        status = request.GET.get('status', 'on')
        user_id = request.GET.get('user_id')
        print(user_id, 'user_id')
        _status = True if status == 'on' else False

        user = get_object_or_404(User, pk=user_id)

        user.is_superuser = _status

        user.save()

        return redirect(reverse('admin'))


class ClientUserView(View):
    TEMPLATE = 'dashboard/auth/client_user.html'

    def get(self, request):
        users = ClientUser.objects.all()
        data = {
            "users": users
        }
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        user_id = request.POST.get('userId')
        print(user_id)
        user = ClientUser.objects.get(pk=user_id)
        user.update_status()
        return JsonResponse({'code': 0, 'msg': 'success'})
