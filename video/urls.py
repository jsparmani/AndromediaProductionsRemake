from django.urls import path
from . import views

app_name = 'video'

urlpatterns = [
    path('import-all/<str:channel_id>/', views.import_all, name='import_all'),
    path('channel/<str:channel_id>/',
         views.ChannelVideosView.as_view(), name='video_channel'),
    path('playlist/<str:playlist_id>/',
         views.PlaylistVideosView.as_view(), name='video_playlist'),
]
