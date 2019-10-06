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

            if channel_id == channel_id_res:
                super(PlaylistAdmin, self).save_model(
                    request, obj, form, change)
                res = youtube.playlistItems().list(playlist_id=obj.playlist_id,
                                                   part='contentDetails').execute()
                video_ids = []
                for item in res['items']:
                    video_ids.append(item['contentDetails']['videoId'])
                print(video_ids)
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(
                    request, 'The playlist does not belong to your channel')
        except:
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, 'The playlist does not exist')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.register(models.Playlist, PlaylistAdmin)
admin.site.register(models.Video)
