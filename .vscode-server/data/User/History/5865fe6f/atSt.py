from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.crypto import get_random_string
import os

from PIL import Image, ImageFile
from pathlib import Path
#from paramiko import SSHClient, AutoAddPolicy

## Section utilisateurs
def index(request):
    message = {}
    if request.method == 'POST':       
#        filesize = request.cookies.get("filesize")
#        file = request.files["fileToUpload"]
#        print(f"FileSize : {filesize}")
#        print(file)      
        #res = make_response(jsonify(["message": f"{file.filename}"]), 200)
        #return res
        
        uploaded_file = request.FILES['fileToUpload']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        manage_file = manage_import_image(name)
        url = fs.url(name)
        message = {'text': name + " uploaded", 'class': 'bg-primary text-light'}
## lien de référence sur la partie ajax https://www.youtube.com/watch?v=HnTWyfuN_Do&ab_channel=JulianNash
    return render(request, "wiforama/index.html", context={"title": "Wiforama", 'message': message})
#    return render(request, "wiforama/index_v1.html", context={"title": "Wiforama", 'message': message})

## Section administrateur
def listing_image(request):
    #ImageFile.LOAD_TRUNCATED_IMAGES = True
    target_folder=settings.MEDIA_ROOT + "/"
    thumbnail_list = {}
    
#    if request.method == 'GET':
#        if request.GET:
#            manage_admin_image(request)
    if request.method == 'POST':
        if request.POST:
            manage_admin_image(request)           
            
    img_list = os.listdir(target_folder)
    for image in img_list:
        if not 'thumbnail_' in image: 
            new_image = create_thumbnail(image)
            #thumbnail_list[image] = {new_image}
        else:
            thumbnail_list[image] = {image}
    return render(request, "wiforama/wiforama_listing.html", context={"page": "list_wiforama", "title": "Listing Wiforama", 'images': thumbnail_list})    
    
def manage_admin_image(request):
    action = request.POST.get('action')
    image = request.POST.get('img')
    path_file = str(settings.MEDIA_ROOT + "/" + image)
    path_thumb = str(settings.MEDIA_ROOT + "/thumbnail_" + image)
#    target_file = str('/home/pi/upload/' + image)
    target_file = str(settings.MEDIA_ROOT + "/media/" + image)
        
    if action == 'valid':
#        print('##### Validation de la photo : ', image)
        if os.path.isfile(path_file):       
            os.rename(path_file, target_file)
            os.remove(path_thumb)
    elif action == 'delete':
        print('Suppression de la photo : ', image)
        if os.path.isfile(path_file):
            os.remove(path_file)
            os.remove(path_thumb)
    elif action == 'rotate':
        angle = request.GET.get('angle')
        print('Rotation avec Angle')
        if angle == '1':
            print('Rotation Gauche de la photo : ', image)
            angle = 90
        elif angle == '2':
            print('Rotation Droite de la photo : ', image)
            angle = 270
        elif angle == '3':
            print('Rotation 180 de la photo : ', image)
            angle = 180
            
        image = Image.open(path_file)
        rot_img = image.rotate(angle)
        rot_img.save(path_file)
        
        thumbnail = Image.open(path_thumb)
        rot_thumb = thumbnail.rotate(angle)
        rot_thumb.save(path_thumb)
        
def manage_import_image(filename):
    new_file = {}

    ## Path, target
    path = settings.MEDIA_ROOT + "/" 
    file = path + filename

    ## Remove space if exist
    new_name = path + "wiforama_" + get_random_string(length=10)
#    new_name = file.replace(" ", "_").lower()
    os.rename(file, new_name)

    ## Extension du fichier
    change_ext = Path(new_name)
    png_file = change_ext.rename(change_ext.with_suffix('.png'))
    
    ## Change extension file to png
    image = Image.open(png_file)
    image.save(png_file, format="PNG")
    
    new_file['unc_file'] = png_file
    new_file['file'] = Path((png_file)).name
    new_file['thumbnail'] = create_thumbnail(new_file['file'])
          
    return new_file

def create_thumbnail(name_file):  
    ## Definition de la taille du thumbnail
    size = (200, 200)
    target_folder = settings.MEDIA_ROOT + "/"
    target_file = target_folder + 'thumbnail_' + name_file
               
    if not os.path.exists(target_file):
        ## Ouverture de l'image
        thumbnail = Image.open(target_folder + name_file)
        thumbnail.thumbnail(size)
        thumbnail.save(target_file)   
