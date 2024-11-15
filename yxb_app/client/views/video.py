from django.views.generic import View
from django.shortcuts import redirect, reverse, get_object_or_404
from yxb_app.libs.base_render import render_to_response
from yxb_app.model.video import Video
from yxb_app.model.video import FromType
from yxb_app.utils.permission import client_auth
from yxb_app.model.comment import Comment


class ExVideo(View):
    TEMPLATE = 'client/video/ex_video.html'

    def get(self, request):
        videos = Video.objects.exclude(from_to=FromType.custom.value)
        print(FromType.custom, '---------')
        print(videos)
        data = {
            'videos': videos
        }

        return render_to_response(request, self.TEMPLATE, data=data)


class VideoSub(View):
    TEMPLATE = 'client/video/video_sub.html'

    def get(self, request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        user = client_auth(request)

        comments = Comment.objects.filter(video=video, status=True).order_by('-id')

        data = {'video': video, 'user': user, 'comments': comments}

        print(data)
        return render_to_response(request, self.TEMPLATE, data=data)


class HomemadeVideo(View):
    TEMPLATE = 'client/video/ex_video.html'

    def get(self, request):
        videos = Video.objects.exclude(from_to=FromType.youku.value)
        data = {
            'videos': videos
        }

        return render_to_response(request, self.TEMPLATE, data=data)
