from django.shortcuts import render
from video import models as vid_models
import random
from user.models import UploadingUser


def home(request):

    playlists = vid_models.Playlist.objects.all().filter(
        user__email__exact='traversymedia@gmail.com')

    channel_id = UploadingUser.objects.get(
        user__email__exact='traversymedia@gmail.com').channel_id

    videos = vid_models.Video.objects.all()
    videos = random.sample(list(videos), 50)
    return render(request, 'home.html', {'videos': videos, 'playlists': playlists, 'channel_id': channel_id})


def video_play(request, video_id):
    return render(request, 'video_play.html', {'video_id': video_id})


def fault(request):
    return render(request, 'fault.html')
