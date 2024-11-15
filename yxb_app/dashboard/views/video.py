from yxb_app.utils.permission import dashboard_auth
from django.views.generic import View
from yxb_app.libs.base_render import render_to_response
from django.shortcuts import redirect, reverse
from yxb_app.utils.common import check_and_get_video_type, handel_video
from yxb_app.model.video import VideoType, FromType, NationalityType, Video, VideoSub, IdentityType, VideoStar
from yxb_app.model.comment import Comment

class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):
        data = {}
        error = request.GET.get('error', '')
        data['error'] = error
        cus_videos = Video.objects.filter(from_to=FromType.custom.value)
        ex_videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['cus_videos'] = cus_videos
        data['ex_videos'] = ex_videos
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get('info')
        video_id = request.POST.get('video_id')
        print(video_id)
        if video_id:
            revers_path = reverse('video_update', kwargs={'video_id': video_id})

        else:
            revers_path = reverse('external_video')
        if not all([name, image, video_type, from_to, nationality, info]):
            return redirect('{}?error={}'.format(revers_path, '必填字段未填写'))
        result = check_and_get_video_type(VideoType, video_type, message='非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(revers_path, result.get('msg')))

        result = check_and_get_video_type(FromType, from_to, '视频来源错误')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(revers_path, result.get('msg')))

        result = check_and_get_video_type(NationalityType, nationality, '国籍不存在')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(revers_path, result.get('msg')))
        print(video_id, 'video_id')
        if not video_id:
            try:
                Video.objects.create(
                    name=name,
                    image=image,
                    video_type=video_type,
                    from_to=from_to,
                    nationality=nationality,
                    info=info
                )
            except Exception:
                return redirect('{}?error={}'.format(revers_path, result.get('msg')))
        else:
            try:
                video = Video.objects.get(pk=video_id)
                video.name = name
                video.video_type = video_type
                video.nationality = nationality
                video.info = info
                video.image = image
                video.from_to = from_to
                video.save()
            except:
                return redirect('{}?error={}'.format(revers_path, "创建失败"))

        return redirect(reverse('external_video'))


class VideoSubView(View):
    TEMPLATE = 'dashboard/video/video_sub.html'
    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        error = request.GET.get('error', '')
        video = Video.objects.get(pk=video_id)
        data['video'] = video
        data['error'] = error
        comments = Comment.objects.filter(video=video).order_by('-id')
        data['comments'] = comments
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request, video_id):

        number = request.POST.get('number')
        url_format = reverse('video_sub', kwargs={'video_id': video_id})
        videosub_id = request.POST.get('videosub_id')
        video = Video.objects.get(pk=video_id)

        if FromType(video.from_to) == FromType.custom:
            url = request.FILES.get('url')
        else:
            url = request.POST.get('url')
        if not all([url, number]):
            return redirect('{}?error={}'.format(url_format, '缺少必填字段'))
        if FromType(video.from_to) == FromType.custom:
            handel_video(url,video_id,number)
            return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

        if not videosub_id:
            try:
                VideoSub.objects.create(
                    url=url,
                    video=video,
                    number=number
                )
            except:
                return redirect('{}?error={}'.format(url_format, '创建失败'))
        else:
            print('走更新逻辑了么')
            video_sub = VideoSub.objects.get(pk=videosub_id)
            video_sub.url = url
            video_sub.number = number
            video_sub.save()

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoStarView(View):
    @dashboard_auth
    def post(self, request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')

        if not all([name, identity, video_id]):
            return redirect(
                '{}?error={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '缺少必要字段'))

        result = check_and_get_video_type(IdentityType, identity, '身份不存在')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('video_sub'), result.get('msg')))
        video = Video.objects.get(pk=video_id)
        try:
            VideoStar.objects.create(
                video=video,
                name=name,
                identity=identity,
                video_id=video_id
            )
        except:
            return redirect('{}?error={}'.format(reverse('video_sub'), '创建失败'))

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class StarDelete(View):

    def get(self, request, star_id, video_id):
        VideoStar.objects.filter(id=star_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class SubDelete(View):
    def get(self, request, sub_id, video_id):
        VideoSub.objects.filter(id=sub_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoUpdateView(View):
    TEMPLATE = 'dashboard/video/video_update.html'

    def get(self, reqeust, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        data['video'] = video
        print(data['video'], 'data')
        print(data.values())

        return render_to_response(reqeust, self.TEMPLATE, data=data)


class VideoStatusUpdate(View):
    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        video.status = not video.status
        video.save()

        return redirect(reverse('external_video'))
