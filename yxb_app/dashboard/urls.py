from django.urls import path
from .views.base import Index
from .views.auth import Login, Register, AdminManger, LogOut, AdminUpdateStatus,ClientUserView
from .views.video import ExternalVideo, VideoSubView, VideoStarView, StarDelete, SubDelete, VideoUpdateView, \
    VideoStatusUpdate
from .views.comments import Comments

urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),
    path('login', Login.as_view(), name='dashboard_login'),
    path('register', Register.as_view(), name='dashboard_register'),
    path('admin', AdminManger.as_view(), name='admin'),
    path('logout', LogOut.as_view(), name='logout'),
    path('admin/update/status', AdminUpdateStatus.as_view(), name='admin_update_status'),
    path('external/video', ExternalVideo.as_view(), name='external_video'),
    path('video/sub/<int:video_id>', VideoSubView.as_view(), name='video_sub'),
    path('video/star', VideoStarView.as_view(), name='video_star_view'),
    path('video/star/delete/<int:star_id>/<int:video_id>',
         StarDelete.as_view(), name='star_delete'),
    path('video/sub/delete/<int:sub_id>/<int:video_id>', SubDelete.as_view(), name='sub_delete'),
    path('video/update/<int:video_id>', VideoUpdateView.as_view(), name='video_update'),
    path('video/update/status/<int:video_id>', VideoStatusUpdate.as_view(), name='video_status_update'),
    path('comment/status/<int:comment_id>/<int:video_id>',Comments.as_view(),name='comment_update_status'),
    path('client/user', ClientUserView.as_view(), name='dashboard_client_user')
]
