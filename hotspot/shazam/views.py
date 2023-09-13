from datetime import datetime
from django.shortcuts import render
from .models import Playlist
from .forms import WifoForm

def index(request):
    if request.method == "POST":
        chanteur = request.POST.get('FormControlArtiste').lower()
        chanson = request.POST.get('FormControlTitre').lower()
        ## Récupère l'adresse IP du navigateur
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
            
        form = WifoForm(request.POST)
        ## Vérification si tous les champs sont remplis
        if form.is_valid():
            message = {'text': "Votre chanson '" + chanson + "' de " + chanteur + " a été ajouté à la playlist", 'class': 'bg-primary text-light'}
            ## Vérification si la chanson exite déjà dans la base de données
            
            choixMusique = Playlist.objects.filter(artiste=chanteur, titre=chanson)
            if not choixMusique.exists():            
                playlist = Playlist.objects.create(
                    artiste = chanteur,
                    titre = chanson,
                    ipaddress = ip,
                    macaddress = "xx:xx:xx:xx:xx:xx"
                )
            else:
                message = {'text': "Votre musique est déjà présent dans la playlist", 'class': 'bg-warning text-primary'}
        else:
            message = {'text': "Veuillez remplir les deux champs", 'class': 'bg-danger text-light'}
        return render(request, "shazam/index.html", context={"message": message, "title": "Shazam"})

    else:
        form = WifoForm()
    
    return render(request, "shazam/index.html", context={"form": form, "title": "Shazam"})

def musique(request, numero_music):
    print(numero_music)
    if numero_music in ["01"]:
        return render(request, f"shazam/musique-{numero_music}.html")
    return render(request, "shazam/musique_not_found.html")

def listing(request):
    artistes = Playlist.objects.order_by('id')
    if request.GET.get('delete'):
        id = request.GET.get('delete')
        delete_event(request, id)
    return render(request, 'shazam/shazam_list.html', context={'artistes': artistes, "title": "Shazam", "page": "list_shazam"})

def tag_song(request):
    artistes = Playlist.objects.order_by('id')
    return render(request, 'shazam/shazam_list.html', context={'artistes': artistes, "title": "Shazam"})

def delete_event(request, event_id):
    artiste = Playlist.objects.filter(pk=event_id)
    if artiste.exists():
        artiste.delete()