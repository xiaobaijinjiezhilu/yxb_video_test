from django.views.generic import View
from yxb_app.libs.base_render import render_to_response
from django.shortcuts import redirect, reverse


class Index(View):
    TEMPLATE = 'client/index.html'

    def get(self, request):
        return redirect(reverse('client_ex_video'))
