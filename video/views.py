from django.shortcuts import render, redirect
from django.http import HttpResponse
from apiclient.discovery import build
from . import models
from django.views import generic
# Create your views here.


def import_all(request, channel_id):
    api_key = "AIzaSyDahUDOnXFAW0jlIC-gIc1cKt_tLlOXzf4"
    youtube = build('youtube', 'v3', developerKey=api_key)
    res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    print(playlist_id)

    videos = []
    next_page_token = None

    while(True):
        res = youtube.playlistItems().list(playlistId=playlist_id, part='snippet',
                                           maxResults=50, pageToken=next_page_token).execute()
        items = res['items']
        for item in items:
            videos.append(item['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    for video in videos:
        try:
            models.Video.objects.create(
                uploading_user=request.user.uploadingusers,
                video_id=video,
                image_url=f'https://img.youtube.com/vi/{video}/sddefault.jpg'
            )
        except:
            continue

    return redirect('admin:video_video_changelist')


class ChannelVideosView(generic.ListView):
    context_object_name = 'videos'
    template_name = 'video/videos_channel.html'
    paginate_by = 20

    def get_queryset(self):
        qs = models.Video.objects.all().filter(
            uploading_user__channel_id__exact=self.kwargs['channel_id'])
        return qs


class PlaylistVideosView(generic.ListView):
    context_object_name = 'videos'
    template_name = 'video/videos_channel.html'
    paginate_by = 20

    def get_queryset(self):
        qs = models.Video.objects.all().filter(
            playlist__playlist_id__exact=self.kwargs['playlist_id'])
        return qs
