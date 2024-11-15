from django.urls import path
from yxb_app.client.views.base import Index
from yxb_app.client.views.video import ExVideo, VideoSub, HomemadeVideo
from yxb_app.client.views.auth import User, Register, LoginOut
from yxb_app.client.views.comment import CommentView

urlpatterns = [
    path('', Index.as_view(), name='client_index'),
    path('video/ex', ExVideo.as_view(), name='client_ex_video'),
    path('video/<int:video_id>', VideoSub.as_view(), name='client_video_sub'),
    path('video/hm', HomemadeVideo.as_view(), name='client_hm_video'),
    path('user/login', User.as_view(), name='client_user'),
    path('user/register', Register.as_view(), name='client_user_register'),
    path('user/logout', LoginOut.as_view(), name='client_user_logout'),
    path('comment/add', CommentView.as_view(), name='comment_add_content')
]
