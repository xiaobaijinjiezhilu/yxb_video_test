from django.views.generic import View
from yxb_app.libs.base_render import render_to_response
from yxb_app.utils.permission import dashboard_auth


class Index(View):
    TEMPLATE = 'dashboard/index.html'

    # @dashboard_auth
    def get(self, request):
        return render_to_response(request, self.TEMPLATE)
