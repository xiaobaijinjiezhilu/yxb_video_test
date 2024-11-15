from django.views.generic import View
from yxb_app.libs.base_render import render_to_response
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from yxb_app.model.video import Video
from yxb_app.model.auth import ClientUser
from yxb_app.models import Comment, ClientUser, Video

class CommentView(View):

    def post(self, request):

        content = request.POST.get('content', '')
        user_id = request.POST.get('userId', '')
        video_id = request.POST.get('videoId', '')

        if not all([content, user_id, video_id]):
            return JsonResponse({'code': -1, 'msg': '缺少必要字段'})

        video = Video.objects.get(pk=int(video_id))
        user = ClientUser.objects.get(pk=int(user_id))
        comment = Comment.objects.create(content=content, video=video, user=user)

        data = {'comment': comment.data()}
        return JsonResponse({'code': 0, 'msg': 'success', 'data': data})
