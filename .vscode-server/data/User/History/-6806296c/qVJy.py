from datetime import datetime
from django.shortcuts import render

def index(request):
    date = datetime.today()
    return render(request, "hotspot/index.html", context={"title": "Accueil"})

def error404(request, exception):
    return render(request, "404.html", context={"title": "Error 404"})