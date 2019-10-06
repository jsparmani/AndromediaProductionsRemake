from django.contrib import admin
from . import models
from apiclient.discovery import build
from django.contrib import messages
api_key = "AIzaSyDahUDOnXFAW0jlIC-gIc1cKt_tLlOXzf4"


class PlaylistAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            "fields": (
                'name', 'playlist_id'
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        youtube = build('youtube', 'v3', developerKey=api_key)
        obj.user = request.user
        uploading_user = obj.user.uploadingusers
        channel_id = uploading_user.channel_id

        try:
            res = youtube.playlists().list(id=obj.playlist_id, part='snippet').execute()
            channel_id_res = res['items'][0]['snippet']['channelId']

        except:
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, 'The playlist does not exist')

        if channel_id == channel_id_res:
            super(PlaylistAdmin, self).save_model(
                request, obj, form, change)
            try:

                video_ids = []
                next_page_token = None

                while(True):

                    res = youtube.playlistItems().list(playlistId=obj.playlist_id,
                                                       part='contentDetails',  maxResults=50, pageToken=next_page_token).execute()

                    for item in res['items']:
                        video_ids.append(item['contentDetails']['videoId'])
                    next_page_token = res.get('nextPageToken')

                    if next_page_token is None:
                        break

                for video in video_ids:
                    models.Video.objects.create(
                        uploading_user=uploading_user,
                        video_id=video,
                        image_url=f'https://img.youtube.com/vi/{video}/sddefault.jpg',
                        playlist=obj
                    )
                print(video_ids)
            except:
                messages.set_level(request, messages.ERROR)
                messages.error(
                    request, 'Server Error')
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, 'The playlist does not belong to your channel')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def delete_model(self, request, obj):
        videos = models.Video.objects.all().filter(
            playlist__playlist_id=obj.playlist_id)
        for video in videos:
            video.delete()
        obj.delete()


class VideoAdmin(admin.ModelAdmin):

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj=obj)
        else:
            return (
                (None, {
                    "fields": (
                        'video_id',
                    ),
                }),
            )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(uploading_user=request.user.uploadingusers)

    def save_model(self, request, obj, form, change):
        obj.uploading_user = request.user.uploadingusers
        youtube = build('youtube', 'v3', developerKey=api_key)
        res = youtube.videos().list(id=obj.video_id,
                                    part='snippet').execute()
        channel_id_res = res['items'][0]['snippet']['channelId']

        if channel_id_res == obj.uploading_user.channel_id:

            image_url = f'https://img.youtube.com/vi/{obj.video_id}/sddefault.jpg'
            obj.image_url = image_url

            super().save_model(request, obj, form, change)

        else:
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, 'The video does not belong to your channel')


admin.site.register(models.Playlist, PlaylistAdmin)
admin.site.register(models.Video, VideoAdmin)
