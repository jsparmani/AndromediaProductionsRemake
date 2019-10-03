from django.contrib import admin
from . import models


class PlaylistAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            "fields": (
                'name', 'playlist_id'
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(PlaylistAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.register(models.Playlist, PlaylistAdmin)
admin.site.register(models.Video)
