from django.shortcuts import render, redirect
from django.http import HttpResponse
from apiclient.discovery import build
from . import models
# Create your views here.


def import_all(request, channel_id):
    api_key = "AIzaSyDahUDOnXFAW0jlIC-gIc1cKt_tLlOXzf4"
    youtube = build('youtube', 'v3', developerKey=api_key)
    res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

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
