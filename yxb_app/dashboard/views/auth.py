from django.views.generic import View
from yxb_app.libs.base_render import render_to_response
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        return render_to_response(request, self.TEMPLATE)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.save()
        return redirect('/dashboard/login')
