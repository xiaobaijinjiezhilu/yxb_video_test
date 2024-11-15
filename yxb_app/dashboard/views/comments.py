from django.views.generic import View
from yxb_app.libs.base_render import render_to_response
from django.http import HttpResponse
from yxb_app.model.comment import Comment
from django.shortcuts import render, redirect, reverse
from yxb_app.model.auth import ClientUser


class Comments(View):

    def get(self, request, comment_id, video_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.status = not comment.status
        comment.save()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))




