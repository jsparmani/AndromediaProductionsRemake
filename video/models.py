from django.db import models
from django.conf import settings


class Video(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    video_id = models.CharField(max_length=255, blank=False)
    image_url = models.URLField(blank=False)
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    playlist = models.ForeignKey(
        'video.Playlist', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.video_id}--{self.user.email}'


class Playlist(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    playlist_id = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.playlist_id}--{self.user.email}'
