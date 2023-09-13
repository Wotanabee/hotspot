from django.db import models
from unixtimestampfield.fields import UnixTimeStampField

# Create your models here.
class Playlist(models.Model):
    artiste = models.CharField(max_length=200)
    titre = models.CharField(max_length=200)
    ipaddress = models.CharField(max_length=45)
    macaddress = models.CharField(max_length=45)
    unixtime = UnixTimeStampField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.artiste
