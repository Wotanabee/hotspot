from django.contrib import admin

# Register your models here.
from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('artiste', 'titre', 'ipaddress', 'macaddress', 'unixtime')



